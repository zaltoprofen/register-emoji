# register-emoji
CUI program to register a emoji in slack

## Installation

## Configuration
Configuration must be written as toml.

Default configuration location is `$HOME/.config/slack.toml`, but this can change by `-c|--configuration-file` option.

### configuration example
```toml
default_team = "your-team"

[your-team]
mail = "smith@example.com"
password = "pass12345"

[other-team]
mail = "john@example.com"
password = "pass54321"
```
