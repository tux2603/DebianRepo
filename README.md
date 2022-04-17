# DebianRepo
Trying to make a little custom debian repository, not much to see here

## Setup

Run the commands to add the repository to your system:

```bash
curl http://deb.tux2603.me/tux2603-ubuntu.gpg | sudo tee /etc/apt/trusted.gpg.d/tux2603-ubuntu.gpg
sudo apt-add-repository "deb http://deb.tux2603.me/ stable main"
sudo apt update
```

## Packages

### cowpower

has a cow pop up and say "Unlimited power" whenever an AC power source is connected

```bash
sudo apt install cowpower
```
