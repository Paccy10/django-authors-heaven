# Authors Haven - A Social platform for the creative at heart.

## Vision

Create a community of like minded authors to foster inspiration and innovation
by leveraging the modern web.

## Requirements

```
- docker
- docker compose V3
- Make (to run Makefile)
```

## Installation and Setup

- Clone the repository

```
git clone https://github.com/Paccy10/django-authors-heaven.git
```

- Environment variables

```
Create a .env file and copy variables from .env.sample to .env and fill them accordingly
```

- Build and run the app

```
make build
```

- Run the app

```
make up
```

- Stop the app

```
make down
```

- View logs

```
make show-logs
```

- Run migrations

```
make migrations
```

- Make migrations

```
make makemigrations
```

- Create a super user

```
make superuser
```

- Bring down containers and delete volumes

```
make down-v
```

- Run tests

```
make test
```

- Check lint errors

```
make flake8
```

- Format code

```
make black
```

- Sort imports

```
make isort
```
