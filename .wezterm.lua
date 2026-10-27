local wezterm = require("wezterm")
local config = wezterm.config_builder()

-- Launch WSL Ubuntu by default.
-- Change "Ubuntu" if your WSL distro has a different name.
config.default_prog = { "wsl.exe", "-d", "Ubuntu", "--cd", "~" }

-- Add launch menu options
config.launch_menu = {
  {
    label = "WSL Ubuntu zsh",
    args = { "wsl.exe", "-d", "Ubuntu", "--cd", "~", "--exec", "zsh", "-l" },
  },
  {
    label = "PowerShell",
    args = { "pwsh.exe", "-NoLogo" },
  },
}

-- Font
config.font = wezterm.font_with_fallback({
  "Monaspace Xenon",
  "JetBrains Mono",
})
config.font_size = 11

-- Appearance
config.color_scheme = 'Gruvbox dark, pale (base16)'
--config.color_scheme = "Gruvbox Dark, medium(base16)" --"Catppuccin Mocha"
config.window_background_opacity = 0.96
config.win32_system_backdrop = "Acrylic"

-- Cursor
config.default_cursor_style = "BlinkingBlock"
config.cursor_blink_rate = 500

-- Tabs
config.hide_tab_bar_if_only_one_tab = false
config.use_fancy_tab_bar = false
config.tab_bar_at_bottom = false

-- Window
config.window_padding = {
  left = 8,
  right = 8,
  top = 6,
  bottom = 6,
}

-- Keybind
config.enable_kitty_keyboard = false

-- Also allow CSI-u style extended key encoding
config.enable_csi_u_key_encoding = false

-- Important on Windows/WSL: avoid Win32 input mode taking precedence
config.allow_win32_input_mode = false

-- For image
config.enable_kitty_graphics = true

-- =========================
-- Agent-friendly behavior
-- =========================

-- Important for long Droid/agent sessions.
config.scrollback_lines = 50000
config.scroll_to_bottom_on_input = true
config.enable_scroll_bar = true

-- Keep pasted multiline prompts safer/predictable.
-- Bracketed paste is supported by WezTerm and will be used by programs that enable it.
config.canonicalize_pasted_newlines = "None"

-- Better rendering.
config.front_end = "OpenGL"
config.max_fps = 120
config.animation_fps = 120

-- Don't prompt on window x close
config.window_close_confirmation = "NeverPrompt"

-- Better Windows key behavior
config.keys = {
  {
    key = "t",
    mods = "CTRL|SHIFT",
    action = wezterm.action.SpawnTab("CurrentPaneDomain"),
  },
  {
    key = "w",
    mods = "CTRL|SHIFT",
    action = wezterm.action.CloseCurrentTab({ confirm = false }),
  },
  {
    key = "q",
    mods = "CTRL|SHIFT",
    action = wezterm.action.CloseCurrentPane({ confirm = false }),
  },
  {
    key = "F11",
    mods = "",
    action = wezterm.action.ToggleFullScreen,
  },
  {
    key = "Enter",
    mods = "ALT",
    action = wezterm.action.DisableDefaultAssignment,
  },
  -- Open PowerShell in a new tab
  {
    key = "p",
    mods = "CTRL|SHIFT",
    action = wezterm.action.SpawnCommandInNewTab({
      args = { "pwsh.exe", "-NoLogo" },
    }),
  },
  -- Show launch menu
  {
    key = "l",
    mods = "CTRL|SHIFT",
    action = wezterm.action.ShowLauncher,
  },
  {
    key = 'Space',
    mods = 'CTRL|ALT',
    action = wezterm.action.SendString '\x1b[32;7u'
  }
  -- {
  --   key = "F12",
  --   mods = "",
  --   action = wezterm.action.ShowDebugOverlay,
  -- }
}

wezterm.on('open-uri', function(window, pane, uri)
    -- wezterm.log_info('Clicked URI: ' .. uri)
    local path = uri:match('^file://wsl%.localhost/Ubuntu(/.*)$')
        or uri:match('^file://(/.*)$')

    if not path then
        return -- Keep normal web-link behavior.
    end

    path = path:gsub('[?#].*$', '')
    path = path:gsub('%%(%x%x)', function(hex)
        return string.char(tonumber(hex, 16))
    end)

    local windows_path =
        '\\\\wsl.localhost\\Ubuntu' .. path:gsub('/', '\\')

    -- wezterm.log_info('Explorer path: ' .. windows_path)
    wezterm.background_child_process {
        'explorer.exe',
        '/select,' .. windows_path,
    }

    return false
end)

return config
