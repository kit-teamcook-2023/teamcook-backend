import pymysql as sql
import os
from dotenv import load_dotenv
import datetime

class MySQL():
    def __init__(self):
        load_dotenv(verbose=True)
        self._con = sql.connect(
            host='localhost', 
            user=os.getenv("MYSQL_ID"), 
            password=os.getenv("MYSQL_PW"), 
            db=os.getenv("MYSQL_DB"), 
            charset='utf8mb4'
            )
        self._cur = self._con.cursor()

    def appendWriting(self, title:str, content:str, author:str):
        sql = f"""INSERT INTO `writings`(`title`, `content`, `author`) VALUES('{title}', '{content}', '{author}')"""
        self._cur.execute(sql)
        self._con.commit()

        #테스트용에서만 작동
        sql = f"""SELECT `date` FROM (SELECT * FROM `writings` WHERE `author`='{author}') AS subquery WHERE `title`='{title}' ORDER BY `date` DESC"""
        self._cur.execute(sql)

        row = self._cur.fetchone()
        return row[0].strftime("%y-%m-%d %H:%M:%S")

    
    # frontend 메타데이터에 writing_id를 가지고 있으면 편함
    def appendComment(self, title, comment, author, parent_writing):
        sql = f"""INSERT INTO `comments`(`writing_id`, `content`, `author`) VALUES({parent_writing}, '{comment}', '{author}')"""
        self._cur.execute(sql)
        self._con.commit()

    def getAllWritings(self):
        sql = f"""SELECT `id`, `title`, `author`, `date` FROM `writings`"""
        self._cur.execute(sql)

        rows = self._cur.fetchall()

        ret = []
        for row in rows:
            ret.append({
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'date': row[3].strftime("%y-%m-%d %H:%M:%S")
            })
        
        return ret

    def getWriting(self, title:str=None, author:str=None, time:str=None, id:int=None):
        if id == None:
            sql = f"""SELECT `title`, `content`, `author`, `date`, `id` FROM (SELECT * FROM `writings` WHERE `author`='{author}') AS subquery WHERE `title`='{title}' AND `date`='{time}'"""
        else:
            sql = f"""SELECT `title`, `content`, `author`, `date`, `id` FROM `writings` WHERE `id`='{id}'"""
        
        
        self._cur.execute(sql)

        row = self._cur.fetchone()

        try:
            ret = {
                'write': {
                    'title': row[0],
                    'content': row[1],
                    'author': row[2],
                    'date': row[3].strftime("%y-%m-%d %H:%M:%S")
                },
                'parent': row[4]
            }
        except:
            ret = {}
        return ret

    def getWritingsCount(self):
        sql = f"""SELECT COUNT(*) FROM `writings`"""
        self._cur.execute(sql)
        row = self._cur.fetchone()

        return {'row_count': row[0]}

    def getComments(self, parent_id):
        sql = f"""SELECT `content`, `author`, `date`, `id` FROM comments WHERE `writing_id`='{parent_id}'"""
        self._cur.execute(sql)
        rows = self._cur.fetchall()

        ret = []
        for row in rows:
            ret.append({
                'content': row[0],
                'author': row[1],
                'date': row[2].strftime("%y-%m-%d %H:%M:%S"),
                'id': row[3]
            })

        return ret

    def getLastPost(self, author: str) -> int:
        sql = f"""SELECT `id` FROM `writings` WHERE `author`='{author}' ORDER BY `date` DESC LIMIT 1"""
        self._cur.execute(sql)
        row = self._cur.fetchone()
        return int(row[0])

    def getLastComment(self, author: str) -> int:
        sql = f"""SELECT `id` FROM `comments` WHERE `author`='{author}' ORDER BY `date` DESC LIMIT 1"""
        self._cur.execute(sql)
        row = self._cur.fetchone()
        return int(row[0])
        
    def deleteWriting(self, id:int):
        # 글 삭제 시 해당 글의 댓글까지 모두 삭제. CASCADE 작동하지 않을 경우 아래의 코드 수행
        # CASCADE 정상 작동 확인. 아래 코드 필요 없음
        # sql = f"""DELETE FROM `comments` WHERE `writing_id`='{id}'"""
        # self._cur.execute(sql)

        sql = f"""DELETE FROM `writings` WHERE `id`='{id}'"""
        self._cur.execute(sql)
        self._con.commit()

    # frontend에서 메타데이터로 댓글 id 저장?
    def deleteComment(self, id:int):
        sql = f"""DELETE FROM `comments` WHERE `id`='{id}'"""
        self._cur.execute(sql)
        self._con.commit()

    def getSearchWritingsCount(self, type:str, data:str):
        sql = f"""SELECT COUNT(*) FROM `writings` WHERE {type}='{data}'"""
        self._cur.execute(sql)
        row = self._cur.fetchone()

        return {'row_count': row[0]}

    def searchWriting(self, type:str, data:str, page:int):
        sql = f"""SELECT `title`, `author`, `date`, `id` FROM `writings` WHERE `{type}` LIKE '%{data}%' ORDER BY `date` DESC LIMIT 20 OFFSET {page*20}"""
        self._cur.execute(sql)
        rows = self._cur.fetchall()

        ret = []
        for row in rows:
            ret.append({
                'id': row[3],
                'title': row[0],
                'author': row[1],
                'date': row[2].strftime("%y-%m-%d %H:%M:%S")
            })

        return ret

    def deleteUser(self, nickname:str):
        sql = f"""DELETE FROM nicknames WHERE `nickname`='{nickname}'"""
        self._cur.execute(sql)
        self._con.commit()

    def searchNickname(self, nickname:str):
        sql = f"""SELECT COUNT(*) FROM `nicknames` WHERE `nickname`='{nickname}'"""
        self._cur.execute(sql)
        row = self._cur.fetchone()

        if row[0] == 1:
            return True
        return False

    def appendNickname(self, nickname:str):
        sql = f"""INSERT INTO nicknames(`nickname`) VALUES ('{nickname}')"""
        self._cur.execute(sql)
        self._con.commit()

    def getDomainFromAddress(self, address:str):
        sql = f"""SELECT domain FROM ips WHERE address='{address}'"""
        self._cur.execute(sql)
        row = self._cur.fetchone()
        return row[0]

    def clearDatabase(self):
        with self._con.cursor() as cursor:
            cursor.execute("DROP DATABASE IF EXISTS writing_table")
            cursor.execute("CREATE DATABASE writing_table")
        self._con.commit()
        
        # 데이터베이스 선택
        self._con.select_db('writing_table')
        
        # 테이블 생성
        with self._con.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE writings (
                    id INT NOT NULL AUTO_INCREMENT,
                    title VARCHAR(200) NOT NULL,
                    content VARCHAR(10000) NOT NULL,
                    author VARCHAR(20) NOT NULL,
                    `date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (id)
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4
            """)
            cursor.execute("ALTER TABLE writings COMMENT='글'")
            cursor.execute("ALTER TABLE writings AUTO_INCREMENT = 1")

            cursor.execute("""
                CREATE TABLE comments (
                    id INT NOT NULL AUTO_INCREMENT,
                    writing_id INT NOT NULL,
                    content VARCHAR(200) NOT NULL,
                    author VARCHAR(20) NOT NULL,
                    `date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (id),
                    KEY writing_id (writing_id),
                    CONSTRAINT FK_comment_writing_id_writings_id FOREIGN KEY (writing_id) REFERENCES writings (id) ON DELETE CASCADE ON UPDATE RESTRICT
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4
            """)
            cursor.execute("ALTER TABLE comments COMMENT='댓글'")
            cursor.execute("ALTER TABLE comments AUTO_INCREMENT = 1")

            cursor.execute("""
                CREATE TABLE nicknames (
                    id INT NOT NULL AUTO_INCREMENT,
                    nickname VARCHAR(20) NOT NULL,
                    PRIMARY KEY (id)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
            """)
            cursor.execute("ALTER TABLE nicknames COMMENT='닉네임'")
            cursor.execute("ALTER TABLE comments AUTO_INCREMENT = 1")

            cursor.execute("""
                CREATE TABLE ips (
                    id INT NOT NULL AUTO_INCREMENT,
                    address VARCHAR(100) NOT NULL,
                    domain VARCHAR(100) NOT NULL,
                    PRIMARY KEY (id)
                ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4
            """)
            cursor.execute("ALTER TABLE comments COMMENT='주소_IP테이블'")
            cursor.execute("ALTER TABLE comments AUTO_INCREMENT = 1")

            cursor.execute("""
                INSERT INTO nicknames(`nickname`) VALUES ('test1'), ('test2'); 
            """)
            cursor.execute("""
                INSERT INTO ips(address, domain) VALUES ('테스트주소1', 'choijungwoo.iptime.org:80')
            """)

        self._con.commit()
        print("테이블이 성공적으로 생성되었습니다.")

class Test():
    def __init__(self):
        self.mysql = MySQL()

    def appendWriting(self, title:str, content:str, author:str):
        return self.mysql.appendWriting(title,content,author)

    def appendComment(self, title:str, content:str, author:str, parent_writing:int):
        self.mysql.appendComment(title, content, author, parent_writing)

    def getWritingId(self, title:str, author:str, t:str):
        return self.mysql.getWriting(title,author,t)['parent']

    def getSearchWritingsCount(self, type:str, data:str):
        return self.mysql.getSearchWritingsCount(type, data)

    def searchWriting(self, type:str, data:str, page:int):
        return self.mysql.searchWriting(type, data, page)

    def getWritingComments(self, title: str, author: str, time: str):
        ret = {}
        result = self.mysql.getWriting(title,author,time)
        ret['writing'] = result
        try:
            result = self.mysql.getComments(result['parent'])
            ret['comments'] = result
        except:
            ret['comments'] = {}
        return ret

    def deleteWriting(self, id:int):
        self.mysql.deleteWriting(id)

    def deleteComment(self, id:int):
        self.mysql.deleteComment(id)

    def printTemperater(self, title:str, author:str, time:str): 
        ret = self.getWritingComments(title, author, time)
        print("\t제목 metadata - ", ret['writing'])
        print("\t댓글")
        for idx, data in enumerate(ret['comments']):
            print(f"\t\t{idx} - ", data)

    def clearDatabase(self):
        self.mysql.clearDatabase()


if __name__ == "__main__":

    # mysql = MySQL()
    test = Test()

    test.clearDatabase()
    
    title = "test"
    author = "tester"
    content = "testing"

    print("게시글 추가 기능")
    t = test.appendWriting("test", "testing", "tester")
    test.printTemperater(title, author, t)

    print("댓글 추가 기능")
    idx = test.getWritingId(title,author,t)
    for i in range(10):
        it = str(i)
        test.appendComment(title+it, content+it, author+it, idx)

    test.printTemperater(title, author, t)

    print("게시글 조회 기능")
    test.printTemperater(title, author, t)

    search_filter = 'title'
    print("게시글 검색 기능")
    print("\t조건에 맞는 게시글 총 개수: ", test.getSearchWritingsCount(search_filter, title))
    print("\t조건에 맞는 게시글들. 날짜 기준 내림차순 정렬")
    ret = test.searchWriting(search_filter, title, 0)
    for idx, data in enumerate(ret):
        print(f"\t\t{idx} - ", data)

    print("게시글 및 댓글 삭제 기능")
    ret = test.getWritingComments(title, author, t)
    comment_id = ret['comments'][2]['id']
    test.deleteComment(comment_id)
    print(f"\t댓글 삭제 - 댓글 id: {comment_id}\n")
    test.printTemperater(title, author, t)

    print("\n\n\t글 삭제")

    writing_id = ret['writing']['parent']
    test.deleteWriting(writing_id)
    test.printTemperater(title, author, t)
    
