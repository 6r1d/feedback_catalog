# Feedback catalog

This is a Django application that stores user comments regarding the [Iroha 2](https://github.com/hyperledger/iroha/tree/iroha2-lts) [documentation](https://hyperledger.github.io/iroha-2-docs/).

## Installation

This application is using `docker-compose` utility for the ease of use and it only needs a secrets file that is provided separately. You'll need to put the `DJANGO_SECRET` file into the project root directory for it to function normally.

By default, the feedback catalog uses port 80. You can alter it in the `nginx` → `ports` section.
Inside the container, Nginx serves on port 80, while the `ports` section defines connection between the host and container ports.

For example, `8080:80` will connect the `8080` port on the host to the `80` port on the container.
A default configuration is `80:80`, so the internal port 80 is exposed at the port 80.

You'll need to build the project with `docker-compose build` before launch.
After it's built, you can launch it with `docker-compose up -d` for it to work as a daemon or `docker-compose up` to display the logs.

### Autorestart feature

It's important to note that the current config has an `autorestart` flag enabled.
When the machine is rebooted, the container will restart without calling it specifically.
If you don't need it, please edit your copy of `docker-compose.yml` and disable the autorestart feature for each separate container (currently `backend` and `nginx`).

## Logging in

The admin account initially has the `admin` password. It is recommended to change it right after the installation.
Assuming the code is running on [`127.0.0.1`](http://127.0.0.1/), go to the admin page at [`127.0.0.1/admin/`](http://127.0.0.1/admin/) and press "change password" in the top right corner.