from rich import print

def printHelp()->None:
    print("[white on blue]1: encode files[/white on blue]")
    print("[white on blue]To make a bs9 file, you need to select a text file, html file , javascript file or more like this.\n[/white on blue]")
    print("[white on blue]2: decode files[/white on blue]")
    print("[white on blue]To decode a bs9 file, you need to select a bs9 file, make sure it's a valid bs9 file and encoded by this program of this version.\n[/white on blue]")
    print("[white on blue]3: show data[/white on blue]")
    print("[white on blue]Display the character data table used to encode and decode.\n[/white on blue]")
    print("[white on blue]4: make bs9pack[/white on blue]")
    print("[white on blue]To make a bs9pack, you need to select a folder, make sure it's a valid folder with files in it and if it's a website folder, it should contain a index.html file.\n[/white on blue]")
    print("[white on blue]5: unpack bs9pack[/white on blue]")
    print("[white on blue]To unpack a bs9pack, you need to select a bs9pack file, make sure it's a valid bs9pack file and encoded by this program of this version.\n[/white on blue]")
    print("[white on blue]6: encode texts[/white on blue]")
    print("[white on blue]To encode the text you entered, also support chinese but won't convert to numbers.\n[/white on blue]")
    print("[white on blue]7: decode bs9 texts[/white on blue]")
    print("[white on blue]To decode the bs9 texts you entered, make sure the version of the encoded text is supported to this decoder.\n[/white on blue]")
    print("[white on blue]8: exit[/white on blue]")
    print("[white on blue]Exit the program with code 0 (normal).\n[/white on blue]")