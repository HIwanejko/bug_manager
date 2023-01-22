# Bug Manager

## Install
``` make install ```

## Initialization

To initialize the application run these steps:
 * ```make migrate```
 * ```make make-migrations```

## Configurations
To test locally you must set an environment variable.
You must set the SECRET_KEY variable as it is required by the settings.
This can be set to anything as it is only used locally.

To set the variable:
 * ` export SECRET_KEY='<any_text>' `

## Build the App

To build the container run this step (requires SECRET_KEY):
 * ```make build```

Once build you can now start the application.

## Run
Run local:
 * ` make run `

Run using docker (local):
 * ` make up `

Run using docker (in-detached-mode):
 * ` make up-detached `

Stop services:
 * ` make down `
