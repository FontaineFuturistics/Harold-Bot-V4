import json

# Class to handle our config file
class JHandler:
    
    # Initialize config and load the file
    def __init__(self, config_path: str) -> None:
        self.file_path = config_path
        self.config = json.load(open(self.file_path, "r"))

    # Write changes to the file
    def save(self):
        
        # Make the output
        output = str(self.config)
        output = output.replace("'", "\"").replace("True", "true").replace("False", "false") # Reformat
        
        # Write
        of = open(self.file_path, "w")
        of.write(output)
        of.close()

        # Return out of void
        return

    # Handle [] syntax
    def __getitem__(self, index) -> object:
        return self.config[index]


if __name__ == "__main__":
    print("Running config.py")

    con = JHandler("./config/config.json")
    con.save()

    print(con["ENV_PATH"])