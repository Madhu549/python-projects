from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import yaml
import sys , traceback
def send_email_alert(sys_working_dir,log_file_path,env,sprint,pipeline,task_name):
    # verify whether the logfile existed or not
    if (os.path.exists(log_file_path)):

        # reading the log file data
        with open(log_file_path, 'r') as f:
            logs = f.readlines()

        table_rows = ''
    
        # preparing the table rows
        for log in logs:
            log = log.split('    ')
            table_rows += f'''<tr>
                    <td>{log[0]}</td>
                    <td>{log[1]}</td>
                    <td>{log[3]}</td>
                    <td>{log[2]}</td>
                    <td class= '{ "text-success" if log[4].upper() == "SUCCESS" else "text-danger" }' >{log[4].upper()}</td>
                    <td style = '{"font-size: 12px" if len(log[5]) > 20 else ""}'>{log[5].split(']')[1] if ']' in log[5] else log[5]}</td>
                    </tr>'''

        # html file structure
        html = f'''
                <!DOCTYPE html>
                <html lang="en">
                    <head>
                        <style>
                            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100;200;300;400;500;600;700;800;900&display=swap');
                            *{{
                                padding:0;
                                margin:0;
                                box-sizing:border-box;
                                font-family:"Outfit","Segoe UI",sans-serif;
                            }}
                            .container{{
                                margin:.5rem auto;
                                display:grid;
                                place-items:center;
                            }}
                            table{{
                                margin:1rem 0;
                                min-width:60%;
                                border-collapse:collapse;
                                text-align:left;
                            }}
                            tr{{
                                border-bottom:1px solid #ADADAD;
                            }}
                            td,th{{
                                padding:.5rem;
                                font-size: 0.9rem;
                            }}
                            th{{
                                text-transform:uppercase;
                            }}
                            thead{{
                                background-color:#E60000;
                                color:white;
                                font-weight:500;
                                letter-spacing:2px;
                            }}
                            tbody tr:nth-child(even){{
                                background-color: #C6D0D2;
                            }}
                            tbody tr:nth-child(odd){{
                                background-color:#E8ECED;
                            }}
                            .text-success{{
                                color: #069D4A;
                                font-weight:500;
                            }}
                            .text-danger{{
                                color: #E60000;
                                font-weight:500;
                            }}
                            h1{{
                                font-size:1.1rem;
                                text-align:center;
                                font-weight:500;
                                text-transform:uppercase;
                                margin-top:1rem;
                            }}
                        </style>
                    </head>
                    <body>
                        <h1>{task_name} for Sprint: <span class="text-danger">{sprint}</span> and Environment: <span class="text-danger">{env}</span> </h1>
                        <div class = "container">
                            <table>
                                <thead>
                                <tr>
                                    <th>RowID</th>
                                    <th>Artifact Type</th>
                                    <th>TARGET SERVER</th>
                                    <th>ACTION</th>
                                    <th>STATUS</th>
                                    <th>MESSAGE</th>
                                </tr>
                                </thead>
                                <tbody>{table_rows}</tbody>
                            </table>
                        </div>
                    </body>
                </html>'''

        email_config_path = f'{sys_working_dir}/_edge-wmapps-deploy/wm_deploy_scripts/config_files/email_config.yaml'
        # fetching the email config data from yaml file
        with open(email_config_path, 'r') as f:
            email_config_data = yaml.load(f, Loader=yaml.FullLoader)

        # defining the email parameter's
        if( env[-1].isdigit() ):
            env = env[:len(env)-1]
        to = ['madhubabu.tammu@vodafone.com', 'kotakonda.mahesh@vodafone.com', 'saitheja.pamarty@vodafone.com']#email_config_data[env.upper()]
        cc = []#email_config_data['CC']
        from_addr = email_config_data['FROM']
        server = email_config_data['MAIL_HOST']
        msg = MIMEMultipart("alternative", None, [MIMEText(html, 'html')])

        # setting msg headers
        msg['From'] = from_addr
        msg['To'] = ','.join(to)
        msg['Cc'] = ','.join(cc)
        msg['Subject'] = f'{task_name} Report for Pipeline: {pipeline}'
        
        # adding cc email id's to to email id's
        to.extend(cc)

        # sending email alert
        try:
            with SMTP(server) as mailer:
                mailer.sendmail(from_addr, to, msg.as_string())
        except Exception:
            traceback.print_exc()
            sys.stderr.write("Error While Sending Email Alert\n")
            return "** Error While Sending Email Alert **"

        return 0
    else:
        return 1
