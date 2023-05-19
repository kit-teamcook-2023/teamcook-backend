import pymysql as sql
import os
from dotenv import load_dotenv
import datetime

class UserSQL():
    def __init__(self):
        load_dotenv(verbose=True)
        self._connect_database()
        
    def __del__(self):
        self._con.close()

    def _connect_database(self):
        try:
            self._con.close()
        except:
            None
            
        self._con = sql.connect(
                host='localhost', 
                user=os.getenv("MYSQL_ID"), 
                password=os.getenv("MYSQL_PW"), 
                db=os.getenv("MYSQL_DB_USER"), 
                charset='utf8mb4'
            )
        
    # 모든 sql 쿼리 함수에 @healthcheck 데코레이터 사용 예정
    def healthcheck(func):
        def wrapper(self, *args, **kwargs):
            try:
                self._con.ping()
            except sql.OperationalError as e:
                if e.args[0] == 2006:
                    self._connect_database()
            return func(self, *args, **kwargs)
        return wrapper

    @healthcheck
    def appendWriting(self, title:str, content:str, author:str, board:str = None):
        with self._con.cursor() as cur:
            if board is None:
                board = "free"
        
            sql = f"""INSERT INTO `writings`(`title`, `content`, `author`, `board`) VALUES('{title}', '{content}', '{author}', '{board}')"""
            cur.execute(sql)
            self._con.commit()

            #테스트용에서만 작동
            sql = f"""SELECT `date` FROM (SELECT * FROM `writings` WHERE `author`='{author}') AS subquery WHERE `title`='{title}' ORDER BY `date` DESC"""
            cur.execute(sql)

            row = cur.fetchone()
        return row[0].strftime("%y-%m-%d %H:%M:%S")

    
    # frontend 메타데이터에 writing_id를 가지고 있으면 편함
    @healthcheck
    def appendComment(self, title, comment, author, parent_writing):
        with self._con.cursor() as cur:
            sql = f"""INSERT INTO `comments`(`writing_id`, `content`, `author`) VALUES({parent_writing}, '{comment}', '{author}')"""
            cur.execute(sql)
        self._con.commit()

    @healthcheck
    def getAllWritings(self, board:str = None):
        with self._con.cursor() as cur:
            print(board)
            if board is None or board == "all":
                sql_board = ""
            else:
                sql_board = f"""WHERE `board`='{board}'"""
            sql = f"""SELECT `id`, `title`, `author`, `date`, `board` FROM `writings` {sql_board}"""
            cur.execute(sql)

            rows = cur.fetchall()

        ret = []
        for row in rows:
            ret.append({
                'id': row[0],
                'title': row[1],
                'author': row[2],
                'date': row[3].strftime("%y-%m-%d %H:%M:%S"),
                'board': row[4]
            })
        
        return ret
        
    @healthcheck
    def getWriting(self, title:str=None, author:str=None, time:str=None, id:int=None):
        if id == None:
            sql = f"""SELECT `title`, `content`, `author`, `date`, `id`, `board` FROM (SELECT * FROM `writings` WHERE `author`='{author}') AS subquery WHERE `title`='{title}' AND `date`='{time}'"""
        else:
            sql = f"""SELECT `title`, `content`, `author`, `date`, `id`, `board` FROM `writings` WHERE `id`='{id}'"""
        
        with self._con.cursor() as cur:
            cur.execute(sql)

            row = cur.fetchone()

        try:
            ret = {
                'write': {
                    'title': row[0],
                    'content': row[1],
                    'author': row[2],
                    'date': row[3].strftime("%y-%m-%d %H:%M:%S"),
                    'board': row[5]
                },
                'parent': row[4]
            }
        except:
            ret = {}
        return ret

    @healthcheck
    def getWritingsCount(self, board:str = None):
        with self._con.cursor() as cur:
            if board is None or board == "all":
                sql_board = ""
            else:
                sql_board = f"""WHERE `board`='{board}'"""

            sql = f"""SELECT COUNT(*) FROM `writings` {sql_board}"""
            cur.execute(sql)
            row = cur.fetchone()

        return {'row_count': row[0]}

    @healthcheck
    def getComments(self, parent_id):
        with self._con.cursor() as cur:
            sql = f"""SELECT `content`, `author`, `date`, `id` FROM comments WHERE `writing_id`='{parent_id}'"""
            cur.execute(sql)
            rows = cur.fetchall()

        ret = []
        for row in rows:
            ret.append({
                'content': row[0],
                'author': row[1],
                'date': row[2].strftime("%y-%m-%d %H:%M:%S"),
                'id': row[3]
            })

        return ret

    @healthcheck
    def getLastPost(self, author: str) -> int:
        with self._con.cursor() as cur:
            sql = f"""SELECT `id` FROM `writings` WHERE `author`='{author}' ORDER BY `date` DESC LIMIT 1"""
            cur.execute(sql)
            row = cur.fetchone()
        return int(row[0])

    @healthcheck
    def getLastComment(self, author: str) -> int:
        with self._con.cursor() as cur:
            sql = f"""SELECT `id` FROM `comments` WHERE `author`='{author}' ORDER BY `date` DESC LIMIT 1"""
            cur.execute(sql)
            row = cur.fetchone()
        return int(row[0])

    @healthcheck
    def deleteWriting(self, id:int):
        # 글 삭제 시 해당 글의 댓글까지 모두 삭제. CASCADE 작동하지 않을 경우 아래의 코드 수행
        # CASCADE 정상 작동 확인. 아래 코드 필요 없음
        # sql = f"""DELETE FROM `comments` WHERE `writing_id`='{id}'"""
        # self._cur.execute(sql)

        with self._con.cursor() as cur:
            sql = f"""DELETE FROM `writings` WHERE `id`='{id}'"""
            cur.execute(sql)
        self._con.commit()

    # frontend에서 메타데이터로 댓글 id 저장?
    @healthcheck
    def deleteComment(self, id:int):
        with self._con.cursor() as cur:
            sql = f"""DELETE FROM `comments` WHERE `id`='{id}'"""
            cur.execute(sql)
        self._con.commit()

    @healthcheck
    def getSearchWritingsCount(self, type:str, data:str, board:str = None):
        with self._con.cursor() as cur:
            if board is None or board == "all":
                sql_board = ""
            else:
                sql_board = f"""AND `board`='{board}'"""

            if type == 'author':
                sql = f"""SELECT COUNT(*) FROM `writings` WHERE `{type}`='{data}' {sql_board}"""
            else:
                sql = f"""SELECT COUNT(*) FROM `writings` WHERE `{type}` LIKE '%{data}%' {sql_board}"""
            cur.execute(sql)
            row = cur.fetchone()

        return {'row_count': row[0]}

    @healthcheck
    def searchWriting(self, type:str, data:str, page:int, board:str = None):
        with self._con.cursor() as cur:
            if board is None or board == "all":
                sql_board = ""
            else:
                sql_board = f"""AND `board`='{board}'"""
            
            if type == 'author':
                sql = f"""SELECT `title`, `author`, `date`, `id`, `board` FROM `writings` WHERE `{type}`='{data}' {sql_board} ORDER BY `date` DESC LIMIT 20 OFFSET {page*20}"""
            else:
                sql = f"""SELECT `title`, `author`, `date`, `id`, `board` FROM `writings` WHERE `{type}` LIKE '%{data}%' {sql_board} ORDER BY `date` DESC LIMIT 20 OFFSET {page*20}"""
            cur.execute(sql)
            rows = cur.fetchall()

        ret = []
        for row in rows:
            ret.append({
                'id': row[3],
                'title': row[0],
                'author': row[1],
                'date': row[2].strftime("%y-%m-%d %H:%M:%S"),
                'board': row[4]
            })

        return ret

    @healthcheck
    def deleteUser(self, uid:str):
        with self._con.cursor() as cur:
            sql = f"""DELETE FROM nicknames WHERE `uid`='{uid}'"""
            cur.execute(sql)
        self._con.commit()

    @healthcheck
    def searchNickname(self, nickname:str):
        with self._con.cursor() as cur:
            sql = f"""SELECT COUNT(*) FROM `nicknames` WHERE `nickname`='{nickname}'"""
            cur.execute(sql)
            row = cur.fetchone()

        if row[0] == 1:
            return True
        return False

    @healthcheck
    def appendNickname(self, nickname:str, uid:str):
        with self._con.cursor() as cur:
            sql = f"""INSERT INTO nicknames(`nickname`, `uid`) VALUES ('{nickname}', '{uid}')"""
            cur.execute(sql)
        self._con.commit()

    @healthcheck
    def findUidUSENickname(self, nickname:str):
        with self._con.cursor() as cur:
            sql = f"""SELECT `uid` FROM nicknames WHERE `nickname`='{nickname}'"""
            cur.execute(sql)
            row = cur.fetchone()
        return row[0]

    @healthcheck    
    def findNicknameUSEUid(self, uid: str) -> str:
        with self._con.cursor() as cursor:
            sql = f"""SELECT nickname FROM nicknames WHERE `uid`='{uid}'"""
            cursor.execute(sql)
            res = cursor.fetchone()
        return res[0]

    @healthcheck
    def getDomainFromAddress(self, address:str):
        with self._con.cursor() as cur:
            sql = f"""SELECT domain FROM ips WHERE address='{address}'"""
            cur.execute(sql)
            row = cur.fetchone()
        return row[0]

    @healthcheck
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
                    board VARCHAR(20) NOT NULL,
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
        self.mysql = UserSQL()

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
    
