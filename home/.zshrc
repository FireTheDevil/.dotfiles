# WSL interactive shell; local credentials belong only in shell.local.
export PATH="$HOME/bin:$HOME/.local/bin:/usr/local/bin:$HOME/.bun/bin:$HOME/.browser-use-env/bin:$PATH"
export ZSH="$HOME/.oh-my-zsh"
ZSH_THEME="clean"
plugins=(git)
[ ! -r "$ZSH/oh-my-zsh.sh" ] || source "$ZSH/oh-my-zsh.sh"
[ ! -s "$HOME/.bun/_bun" ] || source "$HOME/.bun/_bun"
export NVM_DIR="$HOME/.nvm"
[ ! -s "$NVM_DIR/nvm.sh" ] || . "$NVM_DIR/nvm.sh"
[ ! -s "$NVM_DIR/bash_completion" ] || . "$NVM_DIR/bash_completion"
export PI_HYPERLINKS=1
export PI_IMAGE_PROTOCOL=kitty
[ ! -r "$HOME/.config/shell.local" ] || . "$HOME/.config/shell.local"
