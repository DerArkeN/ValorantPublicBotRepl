import mysql.connector
import os

from dotenv import load_dotenv

load_dotenv()


def open():
  return mysql.connector.connect(host=os.getenv("HOST"),
                               user=os.getenv("USER"),
                               password=os.getenv("PASSWORD"),
                               database=os.getenv("DATABASE"))


def close(mydb, cursor):
  cursor.close()
  mydb.close()


def user_exists(id):
  mydb = open()
  cursor = mydb.cursor()
  cursor.execute("SELECT COUNT(*) FROM Userdata WHERE ID = (%s)", (id,))
  data = cursor.fetchone()[0]
  if data == 0:
      return False
  elif data == 1:
      return True
  close(mydb, cursor)


def user_exists_puuid(puuid):
  mydb = open()
  cursor = mydb.cursor()
  cursor.execute("SELECT COUNT(*) FROM Userdata WHERE PUUID = (%s)", (puuid,))
  data = cursor.fetchone()[0]
  if data == 0:
      return False
  elif data == 1:
      return True
  close(mydb, cursor)


def channel_exists(channel):
  mydb = open()
  cursor = mydb.cursor()
  cursor.execute("SELECT COUNT(*) FROM LFTData WHERE CHANNEL = (%s)", (channel.id,))
  data = cursor.fetchone()[0]
  if data == 0:
      return False
  elif data == 1:
      return True
  close(mydb, cursor)


def executor_exists(executor):
  mydb = open()
  cursor = mydb.cursor()
  try:
      cursor.execute("SELECT COUNT(*) FROM LFTData WHERE Executor = (%s)", (executor.id,))
  except AttributeError:
      cursor.execute("SELECT COUNT(*) FROM LFTData WHERE Executor = (%s)", (executor,))
  data = cursor.fetchone()[0]
  if data == 0:
      return False
  elif data == 1:
      return True
  close(mydb, cursor)


def create_table():
  mydb = open()
  print(mydb)
  cursor = mydb.cursor()
  cursor.execute(
      "CREATE TABLE IF NOT EXISTS Userdata (ID VARCHAR(100), PUUID VARCHAR(100), Name VARCHAR(100), Tag VARCHAR("
      "100), Role VARCHAR(100))")
  cursor.execute(
      "CREATE TABLE IF NOT EXISTS LFTData (Executor VARCHAR(100), Message VARCHAR(100), Channel VARCHAR(100))")
  mydb.commit()
  close(mydb, cursor)


def insert_userdata(id, valPUUID, valName, valTag, rank):
  mydb = open()
  cursor = mydb.cursor()
  if not user_exists(id):
      if not user_exists_puuid(valPUUID):
          qry = "INSERT INTO Userdata (ID, PUUID, Name, Tag, Role) VALUES (%s, %s, %s, %s, %s)"
          val = (id, valPUUID, valName, valTag, rank.name)
          cursor.execute(qry, val)
          mydb.commit()
          close(mydb, cursor)
          return 0
      else:
          close(mydb, cursor)
          return 1
  else:
      close(mydb, cursor)
      return 2


def insert_lftdata(executor, message, channel):
  mydb = open()
  cursor = mydb.cursor()
  if not executor_exists(executor):
      qry = "INSERT INTO LFTData (Executor, Message, Channel) VALUES (%s, %s, %s)"
      val = (executor, message, channel)
      cursor.execute(qry, val)
      mydb.commit()
      close(mydb, cursor)
      return 0
  else:
      qry = "UPDATE LFTData SET Message = %s, Channel = %s WHERE Executor = %s"
      val = (message, channel, executor)
      cursor.execute(qry, val)
      mydb.commit()
      close(mydb, cursor)
      return 0


def update_rank(id, rank):
  mydb = open()
  cursor = mydb.cursor()
  if user_exists(id):
      qry = "UPDATE Userdata SET Role = %s WHERE ID = %s"
      val = (rank.name, id)
      cursor.execute(qry, val)
      mydb.commit()
  close(mydb, cursor)


def update_name(id, name):
  mydb = open()
  cursor = mydb.cursor()
  if user_exists(id):
      qry = "UPDATE Userdata SET Name = %s WHERE ID = %s"
      val = (name, id)
      cursor.execute(qry, val)
      mydb.commit()
  close(mydb, cursor)


def update_tag(id, tag):
  mydb = open()
  cursor = mydb.cursor()
  if user_exists(id):
      qry = "UPDATE Userdata SET Tag = %s WHERE ID = %s"
      val = (tag, id)
      cursor.execute(qry, val)
      mydb.commit()
  close(mydb, cursor)


def get_puuid(id):
  mydb = open()
  cursor = mydb.cursor()

  cursor.execute("SELECT PUUID FROM Userdata WHERE ID = (%s)", (id,))
  result = cursor.fetchone()[0]

  close(mydb, cursor)
  return result


def get_name(id):
  mydb = open()
  cursor = mydb.cursor()
  if user_exists(id):
      cursor.execute("SELECT Name FROM Userdata WHERE ID = (%s)", (id,))
      result = cursor.fetchone()[0]

      return result
  close(mydb, cursor)


def get_tag(id):
  mydb = open()
  cursor = mydb.cursor()
  if user_exists(id):
      cursor.execute("SELECT Tag FROM Userdata WHERE ID = (%s)", (id,))
      result = cursor.fetchone()[0]

      return result
  close(mydb, cursor)


def get_rank(id):
  mydb = open()
  cursor = mydb.cursor()
  if user_exists(id):
      cursor.execute("SELECT Role FROM Userdata WHERE ID = (%s)", (id,))
      result = cursor.fetchone()[0]

      return result
  close(mydb, cursor)


def get_executor(channel_or_message):
  mydb = open()
  cursor = mydb.cursor()
  cursor.execute("SELECT Executor FROM LFTData WHERE Channel OR Message = (%s)", (channel_or_message,))
  result = cursor.fetchone()[0]
  close(mydb, cursor)
  return result


def get_channel(executor_or_message):
  mydb = open()
  cursor = mydb.cursor()
  cursor.execute("SELECT Channel FROM LFTData WHERE Executor OR Message = (%s)", (executor_or_message,))
  result = cursor.fetchone()[0]
  close(mydb, cursor)
  return result


def get_message(channel_or_executor):
  mydb = open()
  cursor = mydb.cursor()
  cursor.execute("SELECT Message FROM LFTData WHERE Channel OR Executor = (%s)", (channel_or_executor,))
  result = cursor.fetchone()[0]
  close(mydb, cursor)
  return result


def delete_user(id: int):
  mydb = open()
  cursor = mydb.cursor()
  if user_exists(id):
      cursor.execute("DELETE FROM Userdata WHERE ID = (%s)", (id,))
      mydb.commit()
      print("User with ID " + str(id) + " deleted")
  close(mydb, cursor)


def delete_user_puuid(puuid):
  mydb = open()
  cursor = mydb.cursor()
  if user_exists(puuid):
      cursor.execute("DELETE FROM Userdata WHERE ID = (%s)", (puuid,))
      mydb.commit()
      print("User with ID " + str(puuid) + " deleted")
  close(mydb, cursor)


def delete_lftdata(executor_or_message_or_channel):
  mydb = open()
  cursor = mydb.cursor()
  cursor.execute("DELETE FROM LFTData WHERE Executor OR Channel OR Message = (%s)", (executor_or_message_or_channel,))
  mydb.commit()
  close(mydb, cursor)