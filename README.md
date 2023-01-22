# Bug Manger

## Install
``` make install ```

## Configurations
To test locally you must set an environment variable.
You must set the SECRET_KEY variable as it is required by the settings.
This can be set to anything as it is only used locally.

To set the variable:
 * ` export SECRET_KEY='<any_text>' `

## Run
Run local:
 * ` make run `

Run using docker (local):
 * ` make up `

Run using docker (in-detached-mode):
 * ` make up-detached `

Stop services:
 * ` make down `
