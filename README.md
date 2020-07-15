# Apply styles to message senders in group chats

The middleware applies styles to message authors'/senders' names in group chats
to improve message readability.

## Installation

The scripts below requires

```sh
$ ${EFB_DATA_PATH:=$HOME/.ehforwarderbot}
```

To install, first download the repository with

```sh
$ git clone \
  https://github.com/yjyao/efb-middleware-styled-author \
  "${EFB_DATA_PATH}/profiles/default/styled_author"
```

Then add the middleware ID `- styled_author.styled_author.StyledAuthor` to your
EFB config file (`${EFB_DATA_PATH}/profiles/default/config.yaml`),
under the `middlewares:` section.

Your EFB config file should look like

```yaml
master_channel: blueset.telegram
slave_channels:
  - blueset.wechat
middlewares:
  - ... # other middlewares
  - styled_author.styled_author.StyledAuthor
```

You'll need to restart `ehforwarderbot` to activate the middleware.

## Configuration

The middleware supports two styles: _italic_ and **bold**. The default is _italic_. To change the styling,
create/edit `${EFB_DATA_PATH}/profiles/default/styled_author.styled_author.StyledAuthor/config.yaml` as follows:

```yaml
author_style: 'bold' # One of: 'bold', 'italic'
```

After you change the configuration, restart `ehforwarderbot` to apply the changes.
