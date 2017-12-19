#!/usr/bin/env python3
# @AUTHOR: Arthur Valingot
# @DATE: 06/12/2017
from abc import ABC, abstractmethod

# We can use the function chr: int -> str and ord: str -> int   int(x, 2): bin -> int

PADDING_CHR = ' '


class MessageFactory:

    @staticmethod
    def get_message(message_type, object):
        if type(message_type) is not str:
            raise NotImplementedError(
                'Type of argument wrong it has to be a String')
        if message_type == 'KEY_INIT':
            object.type = 0
            message = KeyInitMessage()
        elif message_type == 'KEY_REPLY':
            object.type = 1
            message = KeyReplyMessage()
        elif message_type == 'MESSAGE_RELAY':
            object.type = 2
            message = RelayMessage()
        elif message_type == 'ERROR':
            object.type = 3
            message = ErrorMessage()

        else:
            raise NotImplementedError('Wrong type of message')

        message.feed(object)
        return message

    @staticmethod
    def get_empty_message(message_type):
        if type(message_type) is not str:
            raise NotImplementedError(
                'Type of argument wrong it has to be a String')
        if message_type == 'KEY_INIT':
            message = KeyInitMessage()
        elif message_type == 'KEY_REPLY':
            #object.type = 1
            message = KeyReplyMessage()
        elif message_type == 'MESSAGE_RELAY':
            object.type = 2
            message = RelayMessage(object)
        elif message_type == 'ERROR':
            object.type = 3
            message = ErrorMessage(object)

        else:
            raise NotImplementedError('Wrong type of message')

        return message


class MessageBase(ABC):

    @staticmethod
    def remove_padding(value):
        for i in range(len(value)):
            if value[i] != PADDING_CHR:
                index = i
                break

        return value[index:]

    @staticmethod
    def get_version_type_str(version, type_message):
        bin_version = bin(version)
        bin_type = bin(type_message)

        version_string = bin_version[2:]

        type_string = bin_type[2:]

        len_version = len(version_string)
        len_type = len(type_string)

        while len_version != 4:
            version_string = '0' + version_string
            len_version += 1
        while len_type != 4:
            type_string = '0' + type_string
            len_type += 1

        final_string = '0b' + type_string + version_string
        final_string = chr(int(final_string, 2))

        return final_string

    @staticmethod
    def get_type_version_length(data):
        type_version = ord(data[0])
        bin_type_version = bin(type_version)
        bin_type_version = bin_type_version[2:]
        len_bin_type_version = len(bin_type_version)

        while len_bin_type_version != 8:
            bin_type_version = '0' + bin_type_version
            len_bin_type_version += 1

        message_type = int('0b' + bin_type_version[:4], 2)
        version = int('0b' + bin_type_version[4:], 2)

        length = data[2]

        return version, message_type, length

    @staticmethod
    def add_padding(value, size):
        len_value = len(value)
        string_value = str(value)
        while len_value != size:
            string_value = PADDING_CHR + string_value
            len_value += 1

        return string_value

    @abstractmethod
    def compute_length(self):
        pass


class KeyInitMessage(MessageBase):
    def feed(self, values):
        self.version = values.version
        self.type = values.type
        self.key_id = values.key_id
        self.g = values.g  # g parameter
        self.p = values.p  # p parameter
        self.A = values.A  # A value

    def compute_length(self):
        return str(int((260 + len(self.g)) / 4))

    def encode(self):
        answer = self.get_version_type_str(self.version, self.type)
        answer += PADDING_CHR
        answer += self.compute_length()
        answer += self.key_id

        answer += self.add_padding(self.g, 128)
        answer += self.add_padding(self.p, 128)
        answer += self.add_padding(self.A, 128)

        return answer.encode()

    def decode(self, value):
        value = value.decode()
        self.version, self.type, length = self.get_type_version_length(value)
        self.key_id = str(value[4:8])
        self.g = self.remove_padding(str(value[8:136]))
        self.p = self.remove_padding(str(value[138:264]))
        self.A = self.remove_padding(str(value[264:390]))

        return self


class KeyReplyMessage(MessageBase):
    def feed(self, values):
        self.version = values.version
        self.type = values.type
        self.key_id = values.key_id
        self.B = values.B  # B value respond by bob

    def compute_length(self):
        return str(int(132 / 4))

    def encode(self):
        answer = self.get_version_type_str(self.version, self.type)
        answer += PADDING_CHR
        answer += self.add_padding(self.compute_length(), 2)

        answer += self.add_padding(self.key_id, 4)
        answer += self.add_padding(self.B, 128)

        return answer.encode()

    def decode(self, value):
        value = value.decode()
        self.version, self.type, length = self.get_type_version_length(value)
        self.key_id = self.remove_padding(str(value[4:8]))
        self.B = self.remove_padding(str(value[8:136]))

        return self


class RelayMessage(MessageBase):

    def feed(self, values):
        self.version = values.version
        self.type = values.type
        self.key_id = values.key_id
        self.next_hop = values.next_hop

        # we will fill the message to the next multiple of 8
        len_message = len(values.message)
        self.message = self.add_padding(
            values.message, len_message + 8 - len_message % 8
        )

    def compute_length(self):
        return str(int((4 + 4 + len(self.message)) / 4))

    def encode(self):
        answer = self.get_version_type_str(self.version, self.type)
        answer += PADDING_CHR
        answer += self.add_padding(str(self.compute_length()), 2)
        answer += self.add_padding(self.key_id, 4)
        answer += self.add_padding(self.next_hop, 128)
        answer += self.message

        return answer.encode()

    def decode(self, value):
        value = value.decode()
        self.version, self.type, length = self.get_type_version_length(value)
        self.key_id = self.remove_padding(str(value[4:8]))
        self.next_hop = self.remove_padding(str(value[8:136]))
        self.message = self.remove_padding(str(value[138:]))

        return self


class ErrorMessage(MessageBase):
    def feed(self, values):
        self.version = values.version
        self.type = values.type
        self.error_code = values.error_code

    def compute_length(self):
        return '1'

    def encode(self):
        answer = self.get_version_type_str(self.version, self.type)
        answer += PADDING_CHR
        answer += self.add_padding(str(self.compute_length()), 2)
        # the size of the error code it's just one byte
        answer += str(self.error_code)
        answer += PADDING_CHR

        return answer.encode()

    def decode(self, value):
        value = value.decode()
        self.version, self.type, length = self.get_type_version_length(value)
        self.error_code = str(value[5])

        return self

# Test Case


class Object():
    pass


def test():
    object = Object()
    object.version = 1
    object.type = 1
    object.key_id = 'a'
    object.g = 'test'
    object.p = 'test'
    object.A = 'test'

    message = MessageFactory.get_message('KEY_INIT', object)
    test_key_init = message.encode()

    version, type_message, length = MessageBase.get_type_version_length(
        test_key_init.decode())
    message_try = MessageFactory.get_empty_message('KEY_INIT')
    test_key_init_message = message_try.decode(test_key_init)
    print(type_message)
    print('Key_init test')
    print(test_key_init_message.type)
    print(test_key_init_message.version)
    print(test_key_init_message.key_id)
    print(test_key_init_message.g)
    print(test_key_init_message.p)
    print(test_key_init_message.A)

    object = Object()

    object.version = 1
    object.key_id = 'test'
    object.B = 'test'
    message = MessageFactory.get_message('KEY_REPLY', object)

    test_key_reply = message.encode()
    test_key_reply_message = message.decode(test_key_reply)

    print('Key_reply test')
    print(test_key_reply_message.type)
    print(test_key_reply_message.version)
    print(test_key_reply_message.key_id)
    print(test_key_reply_message.B)

    object = Object()
    object.version = 1
    object.key_id = 'test'
    object.next_hop = '3000'
    object.message = 'testtest'
    message = MessageFactory.get_message('MESSAGE_RELAY', object)

    test_message__relay = message.encode()
    test_message_relay_message = message.decode(test_message__relay)

    print('Message relay test')
    print(test_message_relay_message.type)
    print(test_message_relay_message.version)
    print(test_message_relay_message.key_id)
    print(test_message_relay_message.next_hop)
    print(test_message_relay_message.message)

    object = Object()
    object.version = 1
    object.error_code = 1

    message = MessageFactory.get_message('ERROR', object)
    test_error = message.encode()
    test_error_message = message.decode(test_error)

    print('Error test')

    print(test_error_message.type)
    print(test_error_message.version)
    print(test_error_message.error_code)


if __name__ == "__main__":
    test()
