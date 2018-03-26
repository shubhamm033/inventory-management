class AddEmployeeViaCSV(BaseHandler):

    @cors
    # @auth
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def post(self):
        """
        Requested:
            CSV file
        """
        try:
            arg = self.request.arguments
                        
            # user_id = self.r_id
            # user_id = '6936f6b2ef6d49a282c3d8c86df1617c'
            user_id = '0c1432d60a7648a9b285e1a374f92f49'
            
            file_json = self.request.files
            file_original_name = file_json["file"][0]["filename"]
            
            path = os.getcwd() + "/DemoData/" + 'hello.xlsx'
            with open(path, 'wb') as f:
                f.write(file_json["file"][0]["body"])

            r = pyexcel.SeriesReader(path)
            
            rows = r.to_records()
        except Exception as e:
            print (e.__str__())
            self.write({"success": False,"message": "File not found.","error": e.__str__()})
            self.finish()
            return

        try:
            permissionGranted = False
            user = yield self.coll_user.find_one({"user_id":user_id})
            if user:
                permissionGranted = True
        except Exception as e:
            self.write({"success": False,"message": "Error in checking permission","error": e.__str__()})            
            self.finish()
            return

        if not permissionGranted:
            self.write({"success": False,"message": "No permission"})
            self.finish()
            return

        try:
            header1 = {
                'S.No.': 0,
                'ID No.': 1,
                'Name': 2,
                'Designation': 3,
                'QCI/BOARD': 4,
                'Date of Birth': 5,
                'Mode of appointment': 6,
                'Mob No :': 7,
                'E-mail (QCI)': 8,
                'E-mail ': 9,
                'Emoluments(In lacs p.a.)': 10,
                'Date of initial joining to the organization': 11,
                'Date of confirmation to the post': 12,
                'Due date of confirmation to the post': 13,
                "Father's Name": 14,
                'Date of tenure completion of contract / deputation': 15,
                'Address': 16,
                'Date of present Promotion to the present designation/joining to the present designation': 17,
                'Adhar Card No': 18,
                'PAN NO': 19,
                'PASSPORT NO': 20,
                'Remarks': 21,
                'I CARD VALIDITY': 22,
                'Qualification': 23,
                'Experience': 24
                }
            
            header = {
                0: 'S.No.',
                1: 'ID No.',
                2: 'Name',
                3: 'Designation',
                4: 'QCI/BOARD',
                5: 'Date of Birth',
                6: 'Mode of appointment',
                7: 'Mob No :',
                8: 'E-mail (QCI)',
                9: 'E-mail ',
                10: 'Emoluments(In lacs p.a.)',
                11: 'Date of initial joining to the organization',
                12: 'Date of confirmation to the post',
                13: 'Due date of confirmation to the post',
                14: "Father's Name",
                15: 'Date of tenure completion of contract / deputation',
                16: 'Address',
                17: 'Date of present Promotion to the present designation/joining to the present designation',
                18: 'Adhar Card No',
                19: 'PAN NO',
                20: 'PASSPORT NO',
                21: 'Remarks',
                22: 'I CARD VALIDITY',
                23: 'Qualification',
                24: 'Experience'
                }
            
            new_boards = list()
            already_exist = list()
            new_employee = list()
            for roow in rows:
                row = dict(roow)

                board = row[header[4]]

                check_board = yield self.coll_board.find_one({"sBoard":board.lower()})
                if check_board:
                    bid = check_board["bid"]
                else:
                    bid = uuid.uuid4().hex
                    self.coll_board.insert_one({"sBoard":board.lower(),"Board":board,"bid":bid})
                    new_boards.append(board)
                
                check_employee = yield self.coll_employee.find_one({"qemail":row[header[8]]})
                if check_employee:
                    already_exist.append( row[header[2]] + " " + row[header[8]])
                else: 
                    eid = uuid.uuid4().hex
                    pemail = row[header[8]]
                    pass_id = pemail.split("@")[0]
                    password = hashlib.sha256(pass_id.encode("utf-8")).hexdigest()
                    
                    newemployee = {
                        "IDNo" : row[header[1]],
                        "name": row[header[2]],
                        "designation":row[header[3]],
                        'board': bid,
                        "DoB":datetimeTOepoch(row[header[5]]),
                        "MoA" : row[header[6]],
                        "phone": row[header[7]],
                        "qemail": row[header[8]],
                        "pemail" : row[header[9]],
                        "salary" : row[header[10]],
                        "DoJ":datetimeTOepoch(row[header[11]]),
                        "DoCtP": datetimeTOepoch(row[header[12]]),
                        "DDoCtP": datetimeTOepoch(row[header[13]]),
                        "fname" : row[header[14]],
                        "DoTC" : datetimeTOepoch(row[header[15]]),
                        "address" : row[header[16]],
                        "DoPPtPD" : datetimeTOepoch(row[header[17]]),
                        "aadhar":row[header[18]],
                        "pan":row[header[19]],
                        "passport" :row[header[20]],
                        "remarks":row[header[21]],
                        "ICV":row[header[22]],
                        "qualification":row[header[23]],
                        "exp" : row[header[24]],

                        "password": password,
                        "eid": eid,
                        "created_on": itime(),
                        "avatar_url":"",
                        "avatar_key":"" ,
                        "added_by" : user_id,
                        "version" : 1
                    }
                    self.coll_employee.insert_one(newemployee)
                    new_employee.append( row[header[2]] + " " + row[header[8]])
                    
            # saveactioninlog(
            #         dblogaction=self.log_action,
                #     who=user_id,
                #     action = "added",
                #     what=newform["Details"]["cid"],
                #     what_type = 'form',
                #     where=project_id,
                #     where_type= 'project',
                #     when=new_form["created_on"],
                #     in_project=project_id,
                #     in_org=project_exist["org_id"],
                #     extra_args=[]
                # )

                status = [
                    {"type":"New boards found","value" : new_boards},
                    {"type":"Employees already exist(based on personal email id)","value" : already_exist},
                    {"type":"New employees found","value" : new_employee}
                ]
            
            self.write({"success": True,"message": "Employees saved from CSV " + file_original_name ,"status":status})
        except Exception as e:
            print (e.__str__())
            self.write({"success": False,"message": "Some error in saving form","error": e.__str__()})
        
        self.finish()
        return


