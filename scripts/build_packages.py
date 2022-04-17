import os, shutil, yaml

def get_packages():
    '''
    Gets a list of all the directories in packages/ and their configuration info
    '''
    packages = []
    for package in os.listdir('packages'):
        if os.path.isdir(os.path.join('packages', package)):
            with open(os.path.join('packages', package, 'config.yaml'), 'r') as f:
                config = yaml.safe_load(f)
                packages.append((package, config))

    return packages

def generate_deb_control(config):
    '''
    Generates the debian control file for a package
    '''
    control = f'Package: {config["name"]}\n'
    control += f'Version: {config["version"]}\n'
    control += 'Maintainer: Owen O\'Connor <tux2603@gmail.com>\n'
    control += f'Depends: {", ".join(config["dependencies"])}\n'
    control += f'Architecture: {config["arch"]}\n'
    control += 'Homepage: https://tux2603.me\n'
    control += f'Description: {config["description"]}\n'

    return control

    
if __name__ == '__main__':
    packages = get_packages()

    # Check to make sure that the repo directory exists
    if not os.path.isdir('repo'):
        os.mkdir('repo')
        
    for package, config in packages:
        print(f'Building {package}')

        package_dir = os.path.join('packages', package)

        # Run the packages makefile
        old_cwd = os.getcwd()
        os.chdir(package_dir)
        os.system('make')
        os.chdir(old_cwd)

        # Make a new directory in repo for this package
        build_num = 1

        while True:
            repo_dir = os.path.join('repo', f'{package}_{config["version"]}-{build_num}_{config["arch"]}')
            try:
                os.mkdir(repo_dir)
                break
            except FileExistsError:
                build_num += 1


        # Copy the packages src/ directory into the new repo directory
        for i in os.listdir(os.path.join(package_dir, 'src')):
            shutil.copytree(os.path.join(package_dir, 'src', i), os.path.join(repo_dir, i))

        # generate and write the debian control file
        os.mkdir(os.path.join(repo_dir, 'DEBIAN'))
        with open(os.path.join(repo_dir, 'DEBIAN', 'control'), 'w') as f:
            f.write(generate_deb_control(config))

        # If post installl rules were given, copy them into postinst
        if 'post' in config:
            with open(os.path.join(repo_dir, 'DEBIAN', 'postinst'), 'w') as f:
                f.write(config['post'])

            # Make the postinst executable
            os.chmod(os.path.join(repo_dir, 'DEBIAN', 'postinst'), 0o755)

        # create the deb file
        os.system(f'fakeroot dpkg-deb --build {repo_dir}')