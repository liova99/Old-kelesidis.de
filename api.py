from config import mysql_connect


def team_atendance():
    cur.execute(('SELECT Team, Full FROM attendance_epl_s15 WHERE id=%d') % 5)
    for (Team, Full) in cur:

        Team = Team
        Full = Full
