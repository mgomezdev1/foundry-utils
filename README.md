# foundry-utils

A collection of utilities for creating Foundry assets programmatically

## Stitchings

To run the stitching tool, create the appropriate configuration,
you can follow the example pattern in the `config` folder.

You can also find the specifics for the configuration by inspecting the `stitch.py` file
and looking at the structure of the `Config` class.

Once that is ready, run this command (replacing `CONFIG_FILE` with the path to your configuration file)

```bash
    python stitch.py -c CONFIG_FILE
```

And you're done! If you get any issues about files not existing,
ensure your sources are correctly specified in your configuration.
Each image-json pair should be named the same and differ merely in their extensions.
