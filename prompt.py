#in python 3, raw_input is renamed to input. In python v <3. input does something else.
def prompt(text):
        try:
                return raw_input(text)
        except:
                try:
                        return input(text)

                except:
                        exit()

