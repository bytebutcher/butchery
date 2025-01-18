# i3-workspace-manager

i3-workspace-manager is an interactive command line tool for managing i3 workspaces. With this tool, you can create new workspaces, rename existing ones, delete them, move windows between workspaces, and switch between workspaces. This tool uses rofi for user input, making it easy and convenient to use.

## Usage

```
i3-workspace-manager [OPTION]

Options:
  create    Create a new workspace
  rename    Rename an existing workspace
  delete    Delete an existing workspace
  move      Move a selected window to a selected workspace
  switch    Switch to a selected workspace
  version   Show version number and quit
  help      Display this help message
```

## Installation

This installation guide describes the steps to download and link the i3-workspace-manager tool from GitHub, so that it can be run from anywhere in the command line.

```
cd ~/.local/bin/
curl -LO https://raw.githubusercontent.com/bytebutcher/butchery/refs/heads/main/i3/i3-workspace-manager
chmod +x i3-workspace-manager
```

Make sure that the ```~/.local/bin``` directory is in your ```PATH```. You can add the following line to your ```.bashrc``` or ```.zshrc```:
```
export PATH="$HOME/.local/bin:$PATH"
```

## Keybindings

Here are some suggested keybindings that you can use, but feel free to customize them to your preference.

* Pressing **Mod + F1** enters "workspace mode" where you can create, rename, or delete workspaces using the keys c, r, and d respectively. Pressing Enter or Escape exits this mode.
* Pressing **Mod + Tab** opens a workspace switcher which allows you to switch to another workspace.
* Pressing **Mod + m** allows you to move the current window to another workspace.

The following lines should be placed inside your i3 config file:
```
# manage workspaces
set $mode_workspace workspace:  (c) create, (r) rename, (d) delete 
mode "$mode_workspace" {
	bindsym --release c exec "i3-workspace-manager create", mode "default"	
	bindsym --release r exec "i3-workspace-manager rename", mode "default"
	bindsym --release d exec "i3-workspace-manager delete", mode "default"
    
	# back to normal: Enter or Escape
	bindsym Return mode "default"
	bindsym Escape mode "default"
}
bindsym $mod+F1 mode "$mode_workspace"
bindsym $mod+Tab exec "i3-workspace-manager switch"
bindsym $mod+m exec "i3-workspace-manager move"
```
## Predefined Workspaces

i3-workspace-manager supports the use of predefined workspaces. 
This feature offers these predefined workspaces as options when moving, 
or switching.

To use predefined workspaces, simply add your workspace names to a file named 
`workspaces.lst`. 
This file should be located in the i3-workspace-manager directory. 
The tool will automatically read this file and incorporate these workspaces 
into its functionality.

## Contributions

If you find any bugs or have any suggestions for improvements, please open an issue or submit a pull request.

## License

i3-workspace-manager is licensed under the GPLv3 License. See LICENSE for more information.

