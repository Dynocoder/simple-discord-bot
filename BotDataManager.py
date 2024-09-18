"""
This file defines the BotDataManager object that will have the required methods to load any data for the chatbot along with
other functions like intent matching, answer matching.

Saurav Prashar, 000903720
"""

class ArrayLengthMismatchException(Exception):
    """Custom Exception class to handle array length mismatch in an elegant way!"""

    def __init__(self, questions_length, strings_length):
        super().__init__(f"Array length mismatch: Questions array has {questions_length} items, but answers array has {strings_length} items.")


class BotDataManager():
    """
    Class to manage Bot Logic - loading data, intent matching, and answer matching.
    """

    def __init__(self, intent_file_path: str, answer_file_path:str):
        self.questions = self.__load_data(intent_file_path, True)
        self.answers = self.__load_data(answer_file_path)
        if len(self.questions) != len(self.answers):
            raise ArrayLengthMismatchException(len(self.questions), len(self.answers))


    def answer(self, user_intent: str) -> str:
        user_intent = self.__clean_string(user_intent).lower().strip()

        if user_intent == 'hello':
            return "Hello, How can I help you with you today! I'm a bot who knows ruby"
        elif user_intent == 'goodbye':
            return "Seeya!"


        i = self.__understand(user_intent)
        response = self.__generate(i)
        if (response == -1):
            return "Sorry, I don't know the answer to that!"

        return str(response)


    def __understand(self, user_intent: str) -> int:
        """
        Method to match the input with an intent. Returns the index of the matched intent.

        Args:
            `user_intent` (int): the user asked intent to look for.

        Returns:
            int: index of the matched intent from the `self.questions` list. -1 if no match found.
        """

        for i in range(len(self.questions)):
            if (self.questions[i].lower() == user_intent):
                return i

        return -1


    def __generate(self, intent_index: int) -> int | str:
        """
        Method to return the index of the answer that matches the intent. returns -1 otherwise.
        """

        if (intent_index == -1):
            return -1

        return self.answers[intent_index]


    def __load_data(self, file_path: str, strong_clean: bool = False) -> list[str]:
        """
        Method is responsible for loading chatbot data (intent, response pairs) from a `intent_file_path` provided as an optional argument

        Args:
            `file_path` (str): the path fo the file to load data from.

        Returns:
            list[str]: list with the file entries as values.
        """

        data_list = []
        with open(file_path, 'r',) as reader:
            try:
                data_list = self.__clean_data(reader.readlines(), strong_clean)
            finally:
                reader.close()
        return data_list


    def __clean_data(self, data_list: list[str], strong_clean: bool = False) -> list[str]:
        """
        Method to clean read data from whitespaces and newline characters using `str.strip()`.

        Args:
            `data_list` (list[str]): list to clean the data from.

        Returns:
            list[str]: list with clean data.
        """

        for i in range(len(data_list)):
            data_list[i] = data_list[i].strip()
            if (strong_clean):
                data_list[i] = self.__clean_string(data_list[i])

        return data_list

    def __clean_string(self, data: str) -> str:
        """Method to remove the special characters from a string."""
        special_chars = "!@#$%^&*()_+=_,'~`<>/|?"

        i = 0;
        l = len(data)
        while i < l:
            if data[i] in special_chars:
                data = data.replace(data[i], "")
                l = len(data)
            i += 1;

        print(data)
        return data



if __name__ == "__main__":
    a = BotDataManager('./intents.txt', './answers.txt')
    print(a.answer("What is Ruby on Rails?"))

