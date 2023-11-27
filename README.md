# HandshakeSurveyResults
 Automatically download individual Handshake (joinhandshake) survey results
See [Setup](#setup) for the necessary setup for these scripts to run automatically.
## Setup

1. Ensure all [dependencies](#dependencies) are configured and running properly
2. Clone the repository
    - If installing from github, use 
        ```bash
        -git clone https://github.com/CLDC-OU/HandshakeSurveyResults.git
        ```
3. Configure the [Environmental Variables](#environmental-variables)
4. Configure [Config](#configuring-config)
5. Run [main.py](main.py)

## Dependencies

### Chromium Driver
- Download the most recent version [here](https://googlechromelabs.github.io/chrome-for-testing/). 
    - Select Stable
    - Open the URL of the chromedriver binary for your system
- Place it in a location that is easy to access. Remember this location because it will be needed in the next step.

> [!NOTE]
> 
> The `chrome` binary is not needed. Only the `chromedriver` binary is needed for this script.

### Python Dependencies

This script uses the python-dotenv and selenium packages which may not be installed by default in your python installation. Run the following commands in the terminal to install.

```shell
python -m pip install python-dotenv
python -m pip install selenium
```

## Environmental Variables

See an example [Here](#example-env)

> [!INFO]
> 
> It is recommended that you create a dedicated Handshake account using an extra email address to access the survey results. Make sure to setup this Handshake account as a Career Services staff member with the "Surveys" Role.

1. Create a file called ".env" in the root of the project directory.
2. Add the following environmental variables:
    - `HS_USERNAME`: The username of the Handshake account that will be downloading the survey results
    - `HS_PASSWORD`: The password of the Handshake account that will be downloading the survey results
    - (optional) `INSTITUTIONAL_EMAIL` - TRUE if `HS_USERNAME` refers to an institutional email address (e.g. oakland.edu). FALSE or omitted otherwise.


### Configuring Config

See an example [Here](#example-config)

The following keys are required for the survey config:
- `downloads_dir`: The downloads directory used by Chrome
    - This is likely the same as the default downloads directory for your operating system
    - The default for Windows is `"C:\Users\USER\Downloads"`. 
    - Be sure to escape any backslashes like `"C:\\Users\\USER\\Downloads"`
- `handshake_url`: The url to the homepage of your school/institution's Career Services Handshake page
    - This can be directly copy-pasted from the Home page url
    - It should look something like `https://oakland.joinhandshake.com/edu`
- `chromedriver_path`: The file path to the Chromedriver installed following the instructions here [Chromium Driver](#chromium-driver)
- `surveys`: A list of JSON objects. See below for configuration instructions.

### Adding Surveys

Surveys are JSON objects that contain the following keys:
- `id`: The id of the survey on Handshake. If you go to the survey it should the be 5 numbers at the end of the link 
    - (e.g., for https://oakland.joinhandshake.com/edu/surveys/12345, 12345 would be the id)
    - Make sure that this attribute is formatted as a string and not a number
- `save_dir`: The file directory that the survey should be saved to
- `rename`: A list of JSON objects with the following keys
    - `replace_pattern`: The regex pattern to replace, formatted as a string
    - `replace_with`: The string to replace where there is a regex match
    - There can be any number of these rename objects. Each of them will be applied one at a time, in order

Example Survey Configuration:

```json
{
    "id": "12345",
    "save_dir": "W:\\handshake_data\\survey_results",
    "rename": [
        {"replace_pattern": "surveyresponse_download", "replace_with": "12345_survey_results_"},
        {"replace_pattern": "-.*", "replace_with": ".csv"}
    ]
}
```

### Example .env
See [example.env](example.env) or below for an example of what your [.env](.env) file should look like.

```
HS_USERNAME="handshakeUsername"
HS_PASSWORD="handshakePassword"
INSTITUTIONAL_EMAIL=FALSE
```


### Example Config

See [survey_config.example.json](survey_config.example.json) or below for an example of what your [survey_config.json](survey_config.json) file should look like.

```json
{
    "downloads_dir": "C:\\Users\\USER\\Downloads",
    "handshake_url": "https://oakland.joinhandshake.com",
    "chromedriver_path": "C:\\Users\\USER\\chromedriver-win64",
    "surveys": [
        {
            "id": "12345",
            "save_dir": "W:\\handshake_data\\survey_results",
            "rename": [
                {"replace_pattern": "surveyresponse_download", "replace_with": "12345_survey_results_"},
                {"replace_pattern": "-.*", "replace_with": ".csv"}
            ]
        }
    ]
}
```