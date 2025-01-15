# Linux Toolkit

## bundle

Bundle multiple shell scripts into a single executable. 

## Features

- Bundles multiple shell scripts into a single executable script.
- Optional password protection for bundled scripts.
- In-Memory execution

### Usage
```
Usage: ./bundle [OPTIONS]

Description:
  Bundles multiple shell scripts into a single executable.

Options:
  -s COMMAND:SCRIPT_PATH,...
    Specify a comma-separated list of command:script_path pairs to include in the bundle.

  -o OUTPUT_SCRIPT
    Specify the filename for the generated executable bundle.

  -f
    Force overwriting the output file if it already exists.

  -p
    Prompt for a password that will be used to encrypt the bundled scripts.

  -h
    Display this help message and exit.
```

## Examples

**Create a bundle from a set of bash scripts:**
```bash
# Bundle
$ ./bundle -s speak:speak.sh,quack:quack.sh,moo:moo.sh -o babel.sh

# Execute bundle
$ ./babel.sh
Usage: ./babel.sh [command] [args...]

Available commands:
  speak
  moo
  quack

# Execute specific command in bundle
$ ./babel.sh speak 'Hello, world!'
Hello, world!
```

**Create a password protected bundle:**
```bash
# Bundle
$ ./bundle -p -s speak:speak.sh,quack:quack.sh,moo:moo.sh -o babel.sh
Password: xxx

# Execute password protected bundle (interactive password prompt)
$ ./babel.sh quack 'Hello, world!'
Password: xxx
Quack! Quack!

# Execute password protected bundle (supply password via environment variable)
$ TOKEN=xxx ./babel.sh moo 'Hello, world!'
Moo! Moo!
```

## hl

Highlight specific words or terms in your text output with colors.

### Usage

```
echo "Your text here" | hl --red term1 --blue term2 term3 --green term4
```

### Features

* Highlight multiple terms at once.
* Choose custom colors for each term.

## iter

iter is a flexible and powerful shell script designed to simplify the processing of structured text files in a UNIX-like environment. 

### Usage

```
iter [-f file] [-d delimiter] [-c column_names] <command>
```

### Examples

```
# Pipe into iter and print every line of a csv file
cat data.txt | iter -d ',' -c 'name,namespace' 'echo $name is in $namespace'
```

```
# Print every line of a csv file
iter -f data.txt -d ',' -c 'name,namespace' 'echo $name is in $namespace'
```

```
# Print every line of a text file
iter -f data.txt 'echo $line'
```

## qrtty

**qrtty** generates QR codes directly to the terminal
supporting various types of data like SMS, URLs, Emails, WiFi credentials, vCards, Geolocation, and plain text. 

### Usage

```commandline
Usage: qrtty [OPTION]... [ARGS]...
Generate QR codes directly to the terminal for various types of data.

Types and Parameters:
  sms       [telephone] [message]
  url       [url]
  email     [email] [subject] [body]
  wifi      [ssid] [password] [encryption]
  vcard     [name] [telephone] [email]
  location  [geolocation]
  text      [text]
```

### Examples
```
  qrtty sms +1234567890 'Hello there'
  qrtty email example@email.com 'Subject' 'Email Body'
  qrtty wifi MySSID MyPassword WPA
  qrtty vcard 'John Doe' +1234567890 john@example.com
  qrtty location '40.7128,-74.0060,New York City'
```

