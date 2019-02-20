# Morenz Functions
Just some python functions to access programmatically some of the Montreal Canadiens loyalty program features ready to deploy as Azure functions HTTP triggered

* **twittercode**
Connects to the [Canadiens Twitter](https://twitter.com/canadiensmtl) and retrieves today's code

Requires the the following values in the local.settings.json file

    ```
    "twitter_app_key": "",
    "twitter_app_secret": ""
    ```


* **voucher**
Connects to the [Club1909](https://www.club1909.com) and redeems code submitted in the request as *dailycode* parameter

Requires the the following values in the local.settings.json file
    
    ```
    "club1909_username": "",
    "club1909_password": "",    
    ```


## Installation

* deploy as Azure function

Follow the instructions here to create a Function app in python https://docs.microsoft.com/bs-latn-ba/azure/azure-functions/functions-create-first-azure-function

Deploy the functions in the created function *[your-function-app]*
```bash
func azure functionapp publish [your-function-app] --publish-local-settings
```
or

* run it locally
```bash
source venv/bin/activate
func start
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
This project is licensed under the terms of the [wtfpl](http://www.wtfpl.net/txt/copying/) license.