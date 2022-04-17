# make the main repo pool
pushd repo
mkdir -p pool/main

# copy all the debs into the pool
cp *.deb pool/main

# make the dists list
mkdir -p dists/stable/main/binary-amd64/

# generate and compress the package list
dpkg-scanpackages --arch amd64 pool/main > dists/stable/main/binary-amd64/Packages
gzip -9 <dists/stable/main/binary-amd64/Packages >dists/stable/main/binary-amd64/Packages.gz

# create the Release file
cat <<EOF >dists/stable/Release
Origin: tux2603's Repository
Label: tux2603's Repository
Suite: stable
Codename: stable
Version: 1.0
Architectures: amd64
Components: main
Description: A collection of programs made by tux2603
EOF
apt-ftparchive release dists/stable/ >>dists/stable/Release

# Sign the release file
gpg --default-key 76A4169E4E701B753387E2C6CB5D8099E5299F06 -abs <dists/stable/Release >dists/stable/Release.gpg
gpg --default-key 76A4169E4E701B753387E2C6CB5D8099E5299F06 -abs --clearsign <dists/stable/Release >dists/stable/InRelease
