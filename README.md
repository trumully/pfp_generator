# Profile Picture Generator
Generate a random profile picture based on given text!

## 🔎 Examples
<table>
    <tr>
        <th><img src="examples/truman.png" alt="truman"/ width="90%"></th>
        <th><img src="examples/trumully.png" alt="trumully" width="90%"/></th>
        <th><img src="examples/github.png" alt="github" width="90%"></th>
        <th><img src="examples/python is awesome.png" alt="python is awesome" width="90%"></th>
    </tr>
    <tr>
        <th>truman</th>
        <th>trumully</th>
        <th>github</th>
        <th>python is awesome</th>
    </tr>
</table>

## 🪄 Quick Start
```shell
pfp-generator [-h] [-s SIZE] [-bg BACKGROUND] [-c COLOR] [-w COLOR_WEIGHT] [--save] [text]

Generate profile pictures.

positional arguments:
  text                  Text to generate the profile picture from. If left blank, generate a random profile picture.

options:
  -h, --help            show this help message and exit
  -s SIZE, --size SIZE  The size of the base pattern. Defaults to 5.
  -bg BACKGROUND, --background BACKGROUND
                        The color of the background.
  -c COLOR, --color COLOR
                        The color of the profile picture.
  -w COLOR_WEIGHT, --color-weight COLOR_WEIGHT
                        The weight of the profile picture color.
  --save                Ask to save the profile picture.
```

## 📦 Setting Up
### Prerequisites
[`pipx`](https://pipx.pypa.io/stable/installation/) or `pip` is required. Using `pipx` is *highly* recommended.

### Installation
With `pipx`:
```shell
pipx install git+https://github.com/trumully/pfp_generator
```

With `pip` (not recommended):
```shell
python -m pip install -U git+https://github.com/trumully/pfp_generator
```

## 🧰 Development
### Prerequisites
Install `poetry` with `pipx`:
```shell
pipx install poetry
```
### Installing
Clone the repository:
```shell
git clone https://github.com/trumully/pfp_generator.git
```
Activate the virtual environment:
```shell
cd pfp_generator
poetry shell
```
Install dependencies:
```shell
poetry install
```

## 🧬 Tests
Run tests with `pytest`
```shell
poetry run pytest
```