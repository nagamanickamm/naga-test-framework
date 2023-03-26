import clr

from naga.test.framework.utils.report_utils import ReportUtils

clr.AddReference("System")
clr.AddReference("System.Security")

import System
from System import Convert
from System.Security.Cryptography import (CryptoStream, CryptoStreamMode, PasswordDeriveBytes, Rijndael, SHA384Managed)
from System.Text import UTF8Encoding


class Encryption:

    def encrypt_text(text):
        utf = UTF8Encoding()
        encryptValue = text + str(len(text))
        for i in range(0, len(text)):
            encryptValue = encryptValue + str(Convert.ToInt16(Convert.ToChar(text[i])))
        passBytes = utf.GetBytes(encryptValue)
        ReportUtils.log("Base 64 string - " + Convert.ToBase64String(SHA384Managed().ComputeHash(passBytes)))
        return Convert.ToBase64String(SHA384Managed().ComputeHash(passBytes))

    def encrypt_with_password(inputData, password):
        bytes = System.Text.Encoding.Unicode.GetBytes(inputData)
        pwdBytes = PasswordDeriveBytes(password, [0x10, 0x40, 0x00, 0x34, 0x1A, 0x70, 0x01, 0x34, 0x56, 0xFF, 0x99, 0x77, 0x4C, 0x22, 0x49])

        encryptedData = Encryption.__encrypt_rijndael(bytes, pwdBytes.GetBytes(16), pwdBytes.GetBytes(16))
        return Convert.ToBase64String(encryptedData)

    def __encrypt_rijndael(inputData, password, values):
        stream = System.IO.MemoryStream()
        rijndael = Rijndael.Create()
        rijndael.Key = password
        rijndael.IV = values
        cStream = CryptoStream(stream, rijndael.CreateEncryptor(rijndael.Key, rijndael.IV), CryptoStreamMode.Write)

        cStream.Write(inputData, 0, len(inputData))
        cStream.Close()
        encryptedData = stream.ToArray()
        return encryptedData
