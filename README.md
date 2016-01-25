csv2properties
==============

This is a simple Python 3 script to help with translation of Java applications.
It lets you write translated strings into a spreadsheet (Google Sheets is
recommended for easy collaboration, but Excel is presumably also possible).
These can subsequently be exported to a CSV file and turned into a bundle of
`.properties` files which are understood by Java.

## Usage

Run the script without arguments for usage instructions.

## Input format

The input spreadsheet should have the following format:

    Key         Description                        _de_DE           _es
    app_name    Name of application    Fart App   
    fart_now    Button text to fart    Fart now    Jetzt furzen!    ¡Pedo ahora!

This will output three files:

    = strings.properties =
    app_name=Fart App
    fart_now=Fart now

    = strings_de_DE.properties =
    fart_now=Jetzt furzen!

    = strings_es.properties =
    fart_now=¡Pedo ahora!

Note:

- The first row is for column headings.
- The second column is for descriptions. These are only for the translators,
  and are ignored by the script.
- The third column _should_ have a blank heading. This represents the empty
  prefix, i.e. the default translation.
- All other column headings should start adhere to the format `_lc` for
  language code, `_lc_cc` for language code and country code, or `_lc_cc_va`
  for language code, country code and variant.
- Empty cells are not copied to the output. This means they can be used to
  explicitly fall back to the default translation. If you actually want to
  include an empty translation in the output file, write `***EMPTY***`.
- Input and output must be in UTF-8 encoding.

## Generating Java code

The script can also generate a Java enum class, to ensure at compile time that
string keys referred to in the source are actually valid:

    package my.awesome.fart.app;

    public enum Strings {
        app_name,
        fart_now,
    }

So instead of `"app_name"`, you would write `Strings.app_name.name()`. You can
also create a helper method which accepts an argument of type `Strings` and
returns the localized string.
