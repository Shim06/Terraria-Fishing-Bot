# Terraria Fishing Bot

Terraria Fishing Bot is a program that uses image recognition to fish automatically in Terraria. The script uses [PyAutoGUI](https://pypi.org/project/PyAutoGUI/) and [OpenCV](https://pypi.org/project/opencv-python/) to scan the screen of any text that come from fishing while using a sonar potion. 

https://github.com/Shim06/Terraria-Fishing-Bot/assets/50046854/47f02e6d-a93a-46e2-8676-038f30ce4a12

## Getting Started

1. Download the RAR file from the releases section.
2. Extract the contents into a directory where you have write permissions.
3. Run `Fishing Bot.exe` to start the program.

## Instructions/How to use

* Ensure that the game is in fullscreen or borderless mode and use the highest game resolution possible.
* Ensure that the fishing area is well-lit and maximize visibility of the sonar potion text, while avoiding any obstructions such as the mouse cursor.
* Configure the Quick Buff function to be bound to the key `B` in the game's keybind settings
* Upon selecting the desired catches, equip your fishing rod of choice and right-click on the desired fishing spot and wait until the bot casts the fishing rod.
* Ensure the correct UI scaling is being used for game. See [UI Scaling Percentage](#UI-Scaling-Percentage) for more information.

## UI Scaling Percentage
Use the given UI Scaling percentages according to your screen resolution:
* 3840 x 2160 - 200%
* 2560 x 1440 - 134%
* 1920 x 1080 - 100%
* 1440 x 900 - 83%
* 1536 x 864 - 80%
* 1366 x 768 - 71%
* 1280 x 720 - 67%

If the resolution is not here, use the following formula to calculate the UI scaling percentage:

`(Screen Resolution / 1080) * 100`

Round off the value to get the UI scaling.

## Why did I make this?

Throughout numerous playthroughs of Terraria with my friends, I consistently assumed the role of the dedicated fisherman within our group. I was responsible for catching fish for crafting buff potions and, notably, wormhole potions. After multiple playthroughs, constantly fishing became quite repetitive, prompting me to find a solution for my problem. I started development on an automatic fishing bot in order to fix this problem.

## Contributing

Contributions are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
