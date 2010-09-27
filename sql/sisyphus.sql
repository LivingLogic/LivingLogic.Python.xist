create sequence SEQ_DBCRONTABLINE
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence SEQ_DGCRONTAB
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence SEQ_DGCRONTABLINE
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence SEQ_DGHOST
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence SEQ_DGJOB
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence SEQ_DGLOGLINE
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence SEQ_DGPARAMETER
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence SEQ_DGPROJECT
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence SEQ_DGRUN
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence SEQ_DGSCRIPT
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence SEQ_DGSCRIPTLINE
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence SEQ_DGUSER
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create table DGHOST
(
	HOST_ID integer not null,
	HOST_NAME varchar2(256 byte) not null,
	HOST_FQDN varchar2(256 byte) not null,
	HOST_IP varchar2(256 byte) not null,
	HOST_SYSNAME varchar2(256 byte),
	HOST_NODENAME varchar2(256 byte),
	HOST_RELEASE varchar2(256 byte),
	HOST_VERSION varchar2(256 byte),
	HOST_MACHINE varchar2(256 byte),
	HOST_CNAME varchar2(64 byte),
	HOST_CDATE timestamp(6) with time zone,
	HOST_UNAME varchar2(64 byte),
	HOST_UDATE timestamp(6) with time zone
);


alter table DGHOST add constraint PK_DGHOST primary key(HOST_ID);


comment on column DGHOST.HOST_ID is '';


comment on column DGHOST.HOST_NAME is '';


comment on column DGHOST.HOST_FQDN is '';


comment on column DGHOST.HOST_IP is '';


comment on column DGHOST.HOST_SYSNAME is '';


comment on column DGHOST.HOST_NODENAME is '';


comment on column DGHOST.HOST_RELEASE is '';


comment on column DGHOST.HOST_VERSION is '';


comment on column DGHOST.HOST_MACHINE is '';


comment on column DGHOST.HOST_CNAME is '';


comment on column DGHOST.HOST_CDATE is '';


comment on column DGHOST.HOST_UNAME is '';


comment on column DGHOST.HOST_UDATE is '';


create table DGUSER
(
	USER_ID integer not null,
	HOST_ID integer not null,
	USER_NAME varchar2(256 byte) not null,
	USER_UID integer,
	USER_GID integer,
	USER_GECOS varchar2(256 byte),
	USER_DIR varchar2(256 byte),
	USER_SHELL varchar2(256 byte),
	USER_CNAME varchar2(64 byte),
	USER_CDATE timestamp(6) with time zone,
	USER_UNAME varchar2(64 byte),
	USER_UDATE timestamp(6) with time zone
);


alter table DGUSER add constraint PK_DGUSER primary key(USER_ID);


comment on column DGUSER.USER_ID is '';


comment on column DGUSER.HOST_ID is '';


comment on column DGUSER.USER_NAME is '';


comment on column DGUSER.USER_UID is '';


comment on column DGUSER.USER_GID is '';


comment on column DGUSER.USER_GECOS is '';


comment on column DGUSER.USER_DIR is '';


comment on column DGUSER.USER_SHELL is '';


comment on column DGUSER.USER_CNAME is '';


comment on column DGUSER.USER_CDATE is '';


comment on column DGUSER.USER_UNAME is '';


comment on column DGUSER.USER_UDATE is '';


create table DGCRONTAB
(
	CRON_ID integer not null,
	USER_ID integer not null,
	CRON_TAB clob,
	CRON_CNAME varchar2(64 byte),
	CRON_CDATE timestamp(6) with time zone
);


alter table DGCRONTAB add constraint PK_DGCRONTAB primary key(CRON_ID);


comment on column DGCRONTAB.CRON_ID is '';


comment on column DGCRONTAB.USER_ID is '';


comment on column DGCRONTAB.CRON_TAB is '';


comment on column DGCRONTAB.CRON_CNAME is '';


comment on column DGCRONTAB.CRON_CDATE is '';


create table DGCRONTABLINE
(
	CTL_ID integer not null,
	CRON_ID integer not null,
	CTL_LINENO integer not null,
	CTL_TYPE integer not null,
	CTL_MINUTE varchar2(32 byte),
	CTL_HOUR varchar2(32 byte),
	CTL_DAYOFMONTH varchar2(32 byte),
	CTL_MONTH varchar2(32 byte),
	CTL_DAYOFWEEK varchar2(32 byte),
	CTL_LINE varchar2(4000 byte),
	CTL_CNAME varchar2(64 byte),
	CTL_CDATE timestamp(6) with time zone
);


alter table DGCRONTABLINE add constraint PK_DGCRONTABLINE primary key(CTL_ID);


comment on column DGCRONTABLINE.CTL_ID is '';


comment on column DGCRONTABLINE.CRON_ID is '';


comment on column DGCRONTABLINE.CTL_LINENO is '';


comment on column DGCRONTABLINE.CTL_TYPE is '';


comment on column DGCRONTABLINE.CTL_MINUTE is '';


comment on column DGCRONTABLINE.CTL_HOUR is '';


comment on column DGCRONTABLINE.CTL_DAYOFMONTH is '';


comment on column DGCRONTABLINE.CTL_MONTH is '';


comment on column DGCRONTABLINE.CTL_DAYOFWEEK is '';


comment on column DGCRONTABLINE.CTL_LINE is '';


comment on column DGCRONTABLINE.CTL_CNAME is '';


comment on column DGCRONTABLINE.CTL_CDATE is '';


create table DGJOB
(
	JOB_ID integer not null,
	PRO_ID integer not null,
	JOB_NAME varchar2(256 byte) not null,
	JOB_ACTIVE integer default 1  not null,
	JOB_LOGFILENAME varchar2(1024 byte),
	JOB_LOGLINKNAME varchar2(1024 byte),
	JOB_PIDFILENAME varchar2(1024 byte),
	JOB_LOG2FILE integer,
	JOB_LOG2DB integer,
	JOB_FORMATLOGLINE varchar2(1024 byte),
	JOB_KEEPFILELOGS integer,
	JOB_KEEPDBLOGS integer,
	JOB_KEEPDBRUNS integer,
	JOB_CNAME varchar2(64 byte),
	JOB_CDATE timestamp(6) with time zone,
	JOB_UNAME varchar2(64 byte),
	JOB_UDATE timestamp(6) with time zone,
	JOB_OVERWRITESCRIPTCONFIG integer default 0  not null
);


alter table DGJOB add constraint PK_DGJOB primary key(JOB_ID);


comment on column DGJOB.JOB_ID is '';


comment on column DGJOB.PRO_ID is '';


comment on column DGJOB.JOB_NAME is '';


comment on column DGJOB.JOB_ACTIVE is '';


comment on column DGJOB.JOB_LOGFILENAME is '';


comment on column DGJOB.JOB_LOGLINKNAME is '';


comment on column DGJOB.JOB_PIDFILENAME is '';


comment on column DGJOB.JOB_LOG2FILE is '';


comment on column DGJOB.JOB_LOG2DB is '';


comment on column DGJOB.JOB_FORMATLOGLINE is '';


comment on column DGJOB.JOB_KEEPFILELOGS is '';


comment on column DGJOB.JOB_KEEPDBLOGS is '';


comment on column DGJOB.JOB_KEEPDBRUNS is '';


comment on column DGJOB.JOB_CNAME is '';


comment on column DGJOB.JOB_CDATE is '';


comment on column DGJOB.JOB_UNAME is '';


comment on column DGJOB.JOB_UDATE is '';


comment on column DGJOB.JOB_OVERWRITESCRIPTCONFIG is '';


create table DGSCRIPT
(
	SCR_ID integer not null,
	JOB_ID integer not null,
	SCR_FILENAME varchar2(1024 byte) not null,
	SCR_SOURCE clob,
	SCR_CNAME varchar2(64 byte),
	SCR_CDATE timestamp(6) with time zone
);


alter table DGSCRIPT add constraint PK_DGSCRIPT primary key(SCR_ID);


comment on column DGSCRIPT.SCR_ID is '';


comment on column DGSCRIPT.JOB_ID is '';


comment on column DGSCRIPT.SCR_FILENAME is '';


comment on column DGSCRIPT.SCR_SOURCE is '';


comment on column DGSCRIPT.SCR_CNAME is '';


comment on column DGSCRIPT.SCR_CDATE is '';


create table DGRUN
(
	RUN_ID integer not null,
	JOB_ID integer not null,
	USER_ID integer not null,
	RUN_PID integer not null,
	RUN_START timestamp(6),
	RUN_END timestamp(6),
	RUN_ERRORS integer not null,
	RUN_OK integer,
	RUN_RESULT varchar2(1024 byte),
	SCR_ID integer not null,
	CRON_ID integer not null,
	RUN_CNAME varchar2(64 byte),
	RUN_CDATE timestamp(6) with time zone,
	RUN_UNAME varchar2(64 byte),
	RUN_UDATE timestamp(6) with time zone
);


alter table DGRUN add constraint PK_DGRUN primary key(RUN_ID);


comment on column DGRUN.RUN_ID is '';


comment on column DGRUN.JOB_ID is '';


comment on column DGRUN.USER_ID is '';


comment on column DGRUN.RUN_PID is '';


comment on column DGRUN.RUN_START is '';


comment on column DGRUN.RUN_END is '';


comment on column DGRUN.RUN_ERRORS is '';


comment on column DGRUN.RUN_OK is '';


comment on column DGRUN.RUN_RESULT is '';


comment on column DGRUN.SCR_ID is '';


comment on column DGRUN.CRON_ID is '';


comment on column DGRUN.RUN_CNAME is '';


comment on column DGRUN.RUN_CDATE is '';


comment on column DGRUN.RUN_UNAME is '';


comment on column DGRUN.RUN_UDATE is '';


create table DGLOGLINE
(
	LOG_ID integer not null,
	RUN_ID integer not null,
	LOG_LINENO integer,
	LOG_DATE timestamp(6),
	LOG_TAGS varchar2(256 byte),
	LOG_LINE clob,
	LOG_CNAME varchar2(64 byte),
	LOG_CDATE timestamp(6) with time zone
);


alter table DGLOGLINE add constraint PK_DGLOGLINE primary key(LOG_ID);


comment on column DGLOGLINE.LOG_ID is '';


comment on column DGLOGLINE.RUN_ID is '';


comment on column DGLOGLINE.LOG_LINENO is '';


comment on column DGLOGLINE.LOG_DATE is '';


comment on column DGLOGLINE.LOG_TAGS is '';


comment on column DGLOGLINE.LOG_LINE is '';


comment on column DGLOGLINE.LOG_CNAME is '';


comment on column DGLOGLINE.LOG_CDATE is '';


create table DGPARAMETER
(
	PAR_ID integer not null,
	PAR_ACTIVE integer not null,
	PAR_LOG2FILE integer not null,
	PAR_LOG2DB integer not null,
	PAR_LOGFILENAME varchar2(1024 byte) not null,
	PAR_LOGLINKNAME varchar2(1024 byte),
	PAR_PIDFILENAME varchar2(1024 byte) not null,
	PAR_FORMATLOGLINE varchar2(1024 byte) not null,
	PAR_KEEPFILELOGS integer not null,
	PAR_KEEPDBLOGS integer not null,
	PAR_KEEPDBRUNS integer not null,
	PAR_CNAME varchar2(64 byte),
	PAR_CDATE timestamp(6) with time zone,
	PAR_UNAME varchar2(64 byte),
	PAR_UDATE timestamp(6) with time zone
);


alter table DGPARAMETER add constraint PK_DGPARAMETER primary key(PAR_ID);


comment on column DGPARAMETER.PAR_ID is '';


comment on column DGPARAMETER.PAR_ACTIVE is '';


comment on column DGPARAMETER.PAR_LOG2FILE is '';


comment on column DGPARAMETER.PAR_LOG2DB is '';


comment on column DGPARAMETER.PAR_LOGFILENAME is '';


comment on column DGPARAMETER.PAR_LOGLINKNAME is '';


comment on column DGPARAMETER.PAR_PIDFILENAME is '';


comment on column DGPARAMETER.PAR_FORMATLOGLINE is '';


comment on column DGPARAMETER.PAR_KEEPFILELOGS is '';


comment on column DGPARAMETER.PAR_KEEPDBLOGS is '';


comment on column DGPARAMETER.PAR_KEEPDBRUNS is '';


comment on column DGPARAMETER.PAR_CNAME is '';


comment on column DGPARAMETER.PAR_CDATE is '';


comment on column DGPARAMETER.PAR_UNAME is '';


comment on column DGPARAMETER.PAR_UDATE is '';


create table DGPROJECT
(
	PRO_ID integer not null,
	PRO_NAME varchar2(256 byte) not null,
	PRO_CNAME varchar2(64 byte),
	PRO_CDATE timestamp(6) with time zone,
	PRO_UNAME varchar2(64 byte),
	PRO_UDATE timestamp(6) with time zone
);


alter table DGPROJECT add constraint PK_DGPROJECT primary key(PRO_ID);


comment on column DGPROJECT.PRO_ID is '';


comment on column DGPROJECT.PRO_NAME is '';


comment on column DGPROJECT.PRO_CNAME is '';


comment on column DGPROJECT.PRO_CDATE is '';


comment on column DGPROJECT.PRO_UNAME is '';


comment on column DGPROJECT.PRO_UDATE is '';


create table DGSCRIPTLINE
(
	SCL_ID integer not null,
	SCR_ID integer not null,
	SCL_LINENO integer not null,
	SCL_LINE varchar2(4000 byte),
	SCL_CNAME varchar2(64 byte),
	SCL_CDATE timestamp(6) with time zone
);


alter table DGSCRIPTLINE add constraint PK_DGSCRIPTLINE primary key(SCL_ID);


comment on column DGSCRIPTLINE.SCL_ID is '';


comment on column DGSCRIPTLINE.SCR_ID is '';


comment on column DGSCRIPTLINE.SCL_LINENO is '';


comment on column DGSCRIPTLINE.SCL_LINE is '';


comment on column DGSCRIPTLINE.SCL_CNAME is '';


comment on column DGSCRIPTLINE.SCL_CDATE is '';


alter table DGCRONTAB add constraint FK1_DGCRONTAB foreign key (USER_ID) references DGUSER(USER_ID);


alter table DGCRONTABLINE add constraint FK1_DGCRONTABLINE foreign key (CRON_ID) references DGCRONTAB(CRON_ID);


alter table DGHOST add constraint UK1_DGHOST unique(HOST_IP);


alter table DGJOB add constraint UK1_DGJOB unique(PRO_ID, JOB_NAME);


alter table DGLOGLINE add constraint FK1_DGLOGLINE foreign key (RUN_ID) references DGRUN(RUN_ID);


alter table DGPROJECT add constraint UK1_DGPROJECT unique(PRO_NAME);


alter table DGRUN add constraint FK1_DGRUN foreign key (JOB_ID) references DGJOB(JOB_ID);


alter table DGRUN add constraint FK2_DGRUN foreign key (USER_ID) references DGUSER(USER_ID);


alter table DGRUN add constraint FK3_DGRUN foreign key (SCR_ID) references DGSCRIPT(SCR_ID);


alter table DGRUN add constraint FK4_DGRUN foreign key (CRON_ID) references DGCRONTAB(CRON_ID);


alter table DGSCRIPT add constraint FK1_DGSCRIPT foreign key (JOB_ID) references DGJOB(JOB_ID);


alter table DGSCRIPTLINE add constraint FK1_DGSCRIPTLINE foreign key (SCR_ID) references DGSCRIPT(SCR_ID);


alter table DGUSER add constraint FK1_DGUSER foreign key (HOST_ID) references DGHOST(HOST_ID);


alter table DGUSER add constraint UK1_DGUSER unique(HOST_ID, USER_NAME);


create or replace force view DGCRONTABLINE_SELECT as
	select
		ctl_id,
		cron_id,
		ctl_lineno,
		ctl_type,
		ctl_minute,
		ctl_hour,
		ctl_dayofmonth,
		ctl_month,
		ctl_dayofweek,
		ctl_line,
		ctl_cname,
		ctl_cdate
	from
		dgcrontabline
/


create or replace force view DGCRONTAB_SELECT as
	select
	c.cron_id,
	c.user_id,
	u.user_name,
	h.host_id,
	h.host_name,
	h.host_fqdn,
	h.host_ip,
	c.cron_tab,
	c.cron_cname,
	c.cron_cdate
from
	dgcrontab c,
	dguser u,
	dghost h
where
	c.user_id = u.user_id and
	u.host_id = h.host_id
/


create or replace force view DGHOST_SELECT as
	select
		host_id,
		host_name,
		host_fqdn,
		host_ip,
		host_sysname,
		host_nodename,
		host_release,
		host_version,
		host_machine,
		host_cname,
		host_cdate,
		host_uname,
		host_udate
	from
		dghost
/


create or replace force view DGJOB_SELECT as
	select
	j.job_id,
	j.pro_id,
	pr.pro_name,
	j.job_name,
	j.job_active,
	j.job_overwritescriptconfig,
	nvl(j.job_log2file, p.par_log2file) as job_log2file,
	nvl(j.job_log2db, p.par_log2db) as job_log2db,
	nvl(j.job_logfilename, p.par_logfilename) as job_logfilename,
	nvl(j.job_loglinkname, p.par_loglinkname) as job_loglinkname,
	nvl(j.job_pidfilename, p.par_pidfilename) as job_pidfilename,
	nvl(j.job_formatlogline, p.par_formatlogline) as job_formatlogline,
	nvl(j.job_keepfilelogs, p.par_keepfilelogs) as job_keepfilelogs,
	nvl(j.job_keepdblogs, p.par_keepdblogs) as job_keepdblogs,
	nvl(j.job_keepdbruns, p.par_keepdbruns) as job_keepdbruns,
	(select count(*) from dgrun where job_id=j.job_id) as job_countruns,
	(select count(*) from dgrun where job_id=j.job_id and run_ok = 0) as job_countfailedruns,
	j.job_cname,
	j.job_cdate,
	j.job_uname,
	j.job_udate
from
	dgjob j,
	dgproject pr,
	dgparameter p
where
	j.pro_id=pr.pro_id
/


create or replace function XMLESCAPE_CLOB
(
	p_text clob,
	p_inattr integer := 0
)
return clob
as
	v_text clob;
begin
	v_text := replace(p_text, '&', '&amp;');
	v_text := replace(v_text, '<', '&lt;');
	v_text := replace(v_text, '>', '&gt;');
	if p_inattr != 0 then
		v_text := replace(v_text, '''', '&apos;');
		v_text := replace(v_text, '"', '&quot;');
	end if;
	return v_text;
end;

/


create or replace force view DGLOGLINE_SELECT as
	select
		log_id,
		run_id,
		log_lineno,
		log_date,
		log_tags,
		log_line,
		replace(xmlescape_clob(log_line), chr(9), '<span class="tab">&#183;&#160;&#160;</span>') as log_line_html,
		decode(
			regexp_instr(log_tags, '^exc$|^exc,|, exc$|^error$|^error,|, error$'),
			null, 0,
			0, 0,
			1
		) as log_bad,
		log_cname,
		log_cdate
	from
		dglogline
/


create or replace force view DGPARAMETER_SELECT as
	select
		par_id,
		par_active,
		par_log2file,
		par_log2db,
		par_logfilename,
		par_loglinkname,
		par_pidfilename,
		par_formatlogline,
		par_keepfilelogs,
		par_keepdblogs,
		par_keepdbruns,
		par_cname,
		par_cdate,
		par_uname,
		par_udate
	from
		dgparameter
/


create or replace force view DGPROJECT_SELECT as
	select
		pro_id,
		pro_name,
		pro_cname,
		pro_cdate,
		pro_uname,
		pro_udate
	from
		dgproject
/


create or replace force view DGRUN_SELECT as
	select
		r.run_id,
		r.job_id,
		j.job_name,
		p.pro_id,
		p.pro_name,
		r.user_id,
		u.user_name,
		h.host_id,
		h.host_name,
		h.host_fqdn,
		h.host_ip,
		r.run_pid,
		r.run_start,
		r.run_end,
		r.run_errors,
		r.run_ok,
		r.run_result,
		r.scr_id,
		s.scr_filename,
		s.scr_source,
		r.cron_id,
		c.cron_tab,
		r.run_cname,
		r.run_cdate,
		r.run_uname,
		r.run_udate
	from
		dgrun r,
		dguser u,
		dghost h,
		dgjob j,
		dgproject p,
		dgscript s,
		dgcrontab c
	where
		r.user_id=u.user_id and
		u.host_id=h.host_id and
		r.job_id=j.job_id and
		j.pro_id=p.pro_id and
		r.scr_id=s.scr_id(+) and
		r.cron_id=c.cron_id(+)
/


create or replace function XMLESCAPE_VARCHAR2
(
	p_text varchar2,
	p_inattr integer := 0
)
return varchar2
as
	v_text varchar2(32767);
begin
	v_text := replace(p_text, '&', '&amp;');
	v_text := replace(v_text, '<', '&lt;');
	v_text := replace(v_text, '>', '&gt;');
	if p_inattr != 0 then
		v_text := replace(v_text, '''', '&apos;');
		v_text := replace(v_text, '"', '&quot;');
	end if;
	return v_text;
end;

/


create or replace force view DGSCRIPTLINE_SELECT as
	select
		scl_id,
		scr_id,
		scl_lineno,
		scl_line,
		replace(xmlescape_varchar2(scl_line), chr(9), '<span class="tab">&#183;&#160;&#160;</span>') as scl_line_html,
		scl_cname,
		scl_cdate
	from
		dgscriptline
/


create or replace force view DGSCRIPT_SELECT as
	select
	s.scr_id,
	s.job_id,
	j.job_name,
	p.pro_id,
	p.pro_name,
	s.scr_filename,
	s.scr_source,
	s.scr_cname,
	s.scr_cdate
from
	dgscript s,
	dgjob j,
	dgproject p
where
	s.job_id = j.job_id and
	j.pro_id = p.pro_id
/


create or replace force view DGUSER_SELECT as
	select
	u.user_id,
	u.host_id,
	h.host_name,
	h.host_ip,
	h.host_fqdn,
	u.user_name,
	u.user_uid,
	u.user_gid,
	u.user_gecos,
	u.user_dir,
	u.user_shell,
	u.user_cname,
	u.user_cdate,
	u.user_uname,
	u.user_udate
from
	dguser u,
	dghost h
where
	u.host_id = h.host_id
/


create or replace function SCRIPT_FHTML
(
	p_script in clob
)
return clob
as
	c_out clob;
	v_start integer;
	v_end integer;
	v_line varchar2(32000);
	v_count integer;
	procedure write(p_text in clob)
	as
	begin
		if p_text is not null and length(p_text) != 0 then
			dbms_lob.append(c_out, p_text);
		end if;
	end;
	procedure write(p_text in varchar2)
	as
	begin
		if p_text is not null then
			dbms_lob.writeappend(c_out, length(p_text), p_text);
		end if;
	end;
begin
	dbms_lob.createtemporary(c_out, true);
	write('<table border="0" cellpadding="0" cellspacing="0" class="script">');
	if p_script is not null then
		v_end := 0;
		v_count := 1;
		loop
			v_start := v_end + 1;
			v_end := instr(p_script, chr(10), v_start);
			if v_end = 0 then
				v_end := length(p_script) + 1;
			end if;
			v_line := dbms_lob.substr(p_script, v_end - v_start, v_start);
			v_line := xmlescape_varchar2(v_line);
			v_line := replace(v_line, ' ', '&#160;');
			v_line := replace(v_line, chr(9), '<span class="tab">&#183;&#160;&#160;</span>');
			write('<tr><th>');
			write(v_count);
			write('</th><td>');
			if length(trim(v_line)) != 0 then
				write(v_line);
			else
				write('&#160;');
			end if;
			write('</td></tr>');
			if v_end >= length(p_script) then
				exit;
			end if;
			v_count := v_count + 1;
		end loop;
	end if;
	write('</table>');
	return c_out;
end;

/


create or replace function LOG_FTEXT
(
	p_run_id in integer
)
return clob
as
	c_out clob;
	procedure write(p_text in clob)
	as
	begin
		if p_text is not null and length(p_text) != 0 then
			dbms_lob.append(c_out, p_text);
		end if;
	end;
	procedure write(p_text in varchar2)
	as
	begin
		if p_text is not null then
			dbms_lob.writeappend(c_out, length(p_text), p_text);
		end if;
	end;
begin
	dbms_lob.createtemporary(c_out, true);
	for row in (select log_line from dglogline where run_id=p_run_id order by log_lineno) loop
		write(row.log_line);
		write(chr(10));
	end loop;
	return c_out;
end;

/


create or replace function LOG_FHTML
(
	p_run_id in integer
)
return clob
as
	c_out clob;
	procedure write(p_text in clob)
	as
	begin
		if p_text is not null and length(p_text) != 0 then
			dbms_lob.append(c_out, p_text);
		end if;
	end;
	procedure write(p_text in varchar2)
	as
	begin
		if p_text is not null then
			dbms_lob.writeappend(c_out, length(p_text), p_text);
		end if;
	end;
begin
	dbms_lob.createtemporary(c_out, true);
	write('<table border="0" cellpadding="0" cellspacing="0" class="log">');
	for row in (select * from dglogline where run_id=p_run_id order by log_lineno) loop
		if regexp_instr(row.log_tags, '^exc$|^exc,|, exc$|^error$|^error,|, error$')>0 then
			write('<tr class="bad"><th>');
		else
			write('<tr><th>');
		end if;
		write(row.log_lineno);
		write('</th><td class="date">');
		write(to_char(row.log_date, 'DD.MM.YYYY HH24:MI:SS'));
		write('</td><td class="line">');
		write(replace(xmlescape_clob(row.log_line), ' ', '&#160;'));
		write('</td></tr>');
	end loop;
	write('</table>');
	return c_out;
end;

/


create or replace function ABBREV
(
	p_str in clob,
	p_len in integer
)
return varchar2
as
	v_len integer;
	v_lastpos integer;
	v_trailer varchar2(4) := ' ...';
begin
	if p_str is null or length(p_str) <= p_len then
		return p_str;
	else
		v_len := p_len - length(v_trailer);
		v_lastpos := instr(p_str, ' ', v_len, 1);
		if v_lastpos != 0 then
			return substr(p_str, 1, v_lastpos - 1) || v_trailer;
		else
			return substr(p_str, 1, v_len - length(v_trailer)) || v_trailer;
		end if;
	end if;
end;

/


create or replace procedure DGUSER_UPDATE
(
	c_user in varchar2,
	p_user_id in out integer,
	p_host_id in integer := null,
	p_user_name in varchar2 := null,
	p_user_uid in integer := null,
	p_user_gid in integer := null,
	p_user_gecos in varchar2 := null,
	p_user_dir in varchar2 := null,
	p_user_shell in varchar2 := null
)
as
begin

	update dguser set
		host_id = p_host_id,
		user_name = p_user_name,
		user_uid = p_user_uid,
		user_gid = p_user_gid,
		user_gecos = p_user_gecos,
		user_dir = p_user_dir,
		user_shell = p_user_shell,
		user_uname = nvl(c_user, user),
		user_udate = systimestamp
	where
		user_id = p_user_id;
end;

/


create or replace procedure DGUSER_INSERT
(
	c_user in varchar2,
	p_user_id in out integer,
	p_host_id in integer := null,
	p_user_name in varchar2 := null,
	p_user_uid in integer := null,
	p_user_gid in integer := null,
	p_user_gecos in varchar2 := null,
	p_user_dir in varchar2 := null,
	p_user_shell in varchar2 := null
)
as
begin
	if p_user_id is null then
		select seq_dguser.nextval into p_user_id from dual;
	end if;

	insert into dguser
	(
		user_id,
		host_id,
		user_name,
		user_uid,
		user_gid,
		user_gecos,
		user_dir,
		user_shell,
		user_cname,
		user_cdate
	)
	values
	(
		p_user_id,
		p_host_id,
		p_user_name,
		p_user_uid,
		p_user_gid,
		p_user_gecos,
		p_user_dir,
		p_user_shell,
		nvl(c_user, user),
		systimestamp
	);
end;

/


create or replace procedure DGLOGLINE_DELETE
(
	c_user in varchar2,
	p_log_id in integer
)
as
begin
	delete from dglogline where log_id = p_log_id;
end;

/


create or replace procedure DGRUN_DELETE
(
	c_user in varchar2,
	p_run_id in integer
)
as
begin
	for row in (select log_id from dglogline where run_id=p_run_id) loop
		dglogline_delete(c_user, row.log_id);
	end loop;

	delete from dgrun where run_id = p_run_id;
end;

/


create or replace procedure DGUSER_DELETE
(
	c_user in varchar2,
	p_user_id in integer
)
as
begin
	for row in (select run_id from dgrun where user_id=p_user_id) loop
		dgrun_delete(c_user, row.run_id);
	end loop;

	delete from dguser where user_id = p_user_id;
end;

/


create or replace procedure DGSCRIPTLINE_INSERT
(
	c_user in varchar2,
	p_scl_id in out integer,
	p_scr_id in integer := null,
	p_scl_lineno in integer := null,
	p_scl_line in varchar2 := null
)
as
begin
	if p_scl_id is null then
		select seq_dgscriptline.nextval into p_scl_id from dual;
	end if;

	insert into dgscriptline
	(
		scl_id,
		scr_id,
		scl_lineno,
		scl_line,
		scl_cname,
		scl_cdate
	)
	values
	(
		p_scl_id,
		p_scr_id,
		p_scl_lineno,
		p_scl_line,
		nvl(c_user, user),
		systimestamp
	);
end;

/


create or replace procedure DGSCRIPT_MAKELINES
(
	c_user in varchar2,
	p_scr_id in integer,
	p_scr_source in clob
)
as
	v_start integer;
	v_end integer;
	v_scl_id integer;
	v_scl_lineno integer;
begin
	v_end := 0;
	if p_scr_source is not null then
		v_scl_lineno := 1;
		loop
			v_start := v_end + 1;
			v_end := instr(p_scr_source, chr(10), v_start);
			if v_end = 0 then
				v_end := length(p_scr_source) + 1;
			end if;

			v_scl_id := null;
			dgscriptline_insert(
				c_user=>c_user,
				p_scl_id=>v_scl_id,
				p_scr_id=>p_scr_id,
				p_scl_lineno=>v_scl_lineno,
				p_scl_line=>dbms_lob.substr(p_scr_source, v_end - v_start, v_start)
			);
			if v_end >= length(p_scr_source) then
				exit;
			end if;
			v_scl_lineno := v_scl_lineno + 1;
		end loop;
	end if;
end;

/


create or replace procedure DGSCRIPT_INSERT
(
	c_user in varchar2,
	p_scr_id in out integer,
	p_job_id in integer := null,
	p_scr_filename in varchar2 := null,
	p_scr_source in clob := null
)
as
begin
	if p_scr_id is null then
		select seq_dgscript.nextval into p_scr_id from dual;
	end if;

	insert into dgscript
	(
		scr_id,
		job_id,
		scr_filename,
		scr_source,
		scr_cname,
		scr_cdate
	)
	values
	(
		p_scr_id,
		p_job_id,
		p_scr_filename,
		p_scr_source,
		nvl(c_user, user),
		systimestamp
	);

	dgscript_makelines(
		c_user=>c_user,
		p_scr_id=>p_scr_id,
		p_scr_source=>p_scr_source
	);
end;

/


create or replace procedure DGSCRIPTLINE_DELETE
(
	c_user in varchar2,
	p_scl_id in integer
)
as
begin
	delete from dgscriptline where scl_id = p_scl_id;
end;

/


create or replace procedure DGSCRIPT_DELETE
(
	c_user in varchar2,
	p_scr_id in integer
)
as
begin
	for row in (select scl_id from dgscriptline where scr_id=p_scr_id) loop
		dgscriptline_delete(c_user, row.scl_id);
	end loop;

	delete from dgscript where scr_id = p_scr_id;
end;

/


create or replace procedure DGSCRIPTLINE_UPDATE
(
	c_user in varchar2,
	p_scl_id in out integer,
	p_scr_id in integer := null,
	p_scl_lineno in integer := null,
	p_scl_line in varchar2 := null
)
as
begin

	update dgscriptline set
		scr_id = p_scr_id,
		scl_lineno = p_scl_lineno,
		scl_line = p_scl_line
	where
		scl_id = p_scl_id;
end;

/


create or replace procedure DGRUN_UPDATE
(
	c_user in varchar2,
	p_run_id in out integer,
	p_job_id in integer := null,
	p_user_id in integer := null,
	p_run_pid in integer := null,
	p_run_start in timestamp := null,
	p_run_end in timestamp := null,
	p_run_errors in integer := null,
	p_run_ok in integer := null,
	p_run_result in varchar2 := null,
	p_scr_id in integer := null,
	p_cron_id in integer := null
)
as
begin

	update dgrun set
		job_id = p_job_id,
		user_id = p_user_id,
		run_pid = p_run_pid,
		run_start = p_run_start,
		run_end = p_run_end,
		run_errors = p_run_errors,
		run_ok = p_run_ok,
		run_result = p_run_result,
		scr_id = p_scr_id,
		cron_id = p_cron_id,
		run_uname = nvl(c_user, user),
		run_udate = systimestamp
	where
		run_id = p_run_id;
end;

/


create or replace procedure DGCRONTABLINE_INSERT
(
	c_user in varchar2,
	p_ctl_id in out integer,
	p_cron_id in integer := null,
	p_ctl_lineno in integer := null,
	p_ctl_type in integer := null,
	p_ctl_minute in varchar2 := null,
	p_ctl_hour in varchar2 := null,
	p_ctl_dayofmonth in varchar2 := null,
	p_ctl_month in varchar2 := null,
	p_ctl_dayofweek in varchar2 := null,
	p_ctl_line in varchar2 := null
)
as
begin
	if p_ctl_id is null then
		select seq_dgcrontabline.nextval into p_ctl_id from dual;
	end if;

	insert into dgcrontabline
	(
		ctl_id,
		cron_id,
		ctl_lineno,
		ctl_type,
		ctl_minute,
		ctl_hour,
		ctl_dayofmonth,
		ctl_month,
		ctl_dayofweek,
		ctl_line,
		ctl_cname,
		ctl_cdate
	)
	values
	(
		p_ctl_id,
		p_cron_id,
		p_ctl_lineno,
		p_ctl_type,
		p_ctl_minute,
		p_ctl_hour,
		p_ctl_dayofmonth,
		p_ctl_month,
		p_ctl_dayofweek,
		p_ctl_line,
		nvl(c_user, user),
		systimestamp
	);
end;

/


create or replace procedure DGCRONTAB_MAKELINES
(
	c_user in varchar2,
	p_cron_id in integer,
	p_cron_tab in clob
)
as
	v_start integer;
	v_end integer;
	v_inlinestart integer;
	v_inlineend integer;
	v_line varchar2(32000);
	v_part varchar2(32000);
	v_count integer;
	v_ctl_id integer;
	v_ctl_lineno dgcrontabline.ctl_lineno%type;
	v_ctl_type dgcrontabline.ctl_type%type;
	v_ctl_minute dgcrontabline.ctl_minute%type;
	v_ctl_hour dgcrontabline.ctl_hour%type;
	v_ctl_dayofmonth dgcrontabline.ctl_dayofmonth%type;
	v_ctl_month dgcrontabline.ctl_month%type;
	v_ctl_dayofweek dgcrontabline.ctl_dayofweek%type;
	v_ctl_line dgcrontabline.ctl_line%type;
begin
	v_end := 0;
	if p_cron_tab is not null then
		v_ctl_lineno := 1;
		loop
			-- Preinitialize fields
			v_ctl_minute := null;
			v_ctl_hour := null;
			v_ctl_dayofmonth := null;
			v_ctl_month := null;
			v_ctl_dayofweek := null;

			v_start := v_end + 1;
			v_end := instr(p_cron_tab, chr(10), v_start);
			if v_end = 0 then
				v_end := length(p_cron_tab) + 1;
			end if;

			v_line := dbms_lob.substr(p_cron_tab, v_end - v_start, v_start);
			v_line := regexp_replace(v_line, '^[ \t]*', '');

			if regexp_like(v_line, '^[0-9*]') then -- Line is a real job specification
				v_ctl_type := 1;
				v_inlineend := 0;
				v_count := 1;
				loop
					v_inlinestart := v_inlineend + 1;
					v_inlineend := regexp_instr(v_line, '[ \t]+', v_inlinestart, 1, 1);
					if v_inlineend = 0 or v_count = 6 then
						v_inlineend := length(v_line) + 1;
					else
						v_inlineend := v_inlineend - 1;
					end if;
					v_part := substr(v_line, v_inlinestart, v_inlineend - v_inlinestart);
					v_part := regexp_replace(v_part, '[ \t]*$', '');
					if v_count = 1 then
						v_ctl_minute := v_part;
					elsif v_count = 2 then
						v_ctl_hour := v_part;
					elsif v_count = 3 then
						v_ctl_dayofmonth := v_part;
					elsif v_count = 4 then
						v_ctl_month := v_part;
					elsif v_count = 5 then
						v_ctl_dayofweek := v_part;
					else
						v_ctl_line := v_part;
					end if;
					if v_inlineend >= length(v_line) then
						exit;
					end if;
					v_count := v_count + 1;
				end loop;
			elsif regexp_like(v_line, '^#') then -- Line is a comment
				v_ctl_type := 2;
				v_ctl_line := v_line;
			elsif v_line is null then -- Line is empty
				v_ctl_type := 0;
				v_ctl_line := null;
			else -- Line is (probably) an environment variable assignment
				v_ctl_type := 2;
				v_ctl_line := v_line;
			end if;
			v_ctl_id := null;
			dgcrontabline_insert(
				c_user=>c_user,
				p_ctl_id=>v_ctl_id,
				p_cron_id=>p_cron_id,
				p_ctl_lineno=>v_ctl_lineno,
				p_ctl_type=>v_ctl_type,
				p_ctl_minute=>v_ctl_minute,
				p_ctl_hour=>v_ctl_hour,
				p_ctl_dayofmonth=>v_ctl_dayofmonth,
				p_ctl_month=>v_ctl_month,
				p_ctl_dayofweek=>v_ctl_dayofweek,
				p_ctl_line=>v_ctl_line
			);
			if v_end >= length(p_cron_tab) then
				exit;
			end if;
			v_ctl_lineno := v_ctl_lineno + 1;
		end loop;
	end if;
end;

/


create or replace procedure DGCRONTAB_INSERT
(
	c_user in varchar2,
	p_cron_id in out integer,
	p_user_id in integer := null,
	p_cron_tab in clob := null
)
as
begin
	if p_cron_id is null then
		select seq_dgcrontab.nextval into p_cron_id from dual;
	end if;

	insert into dgcrontab
	(
		cron_id,
		user_id,
		cron_tab,
		cron_cname,
		cron_cdate
	)
	values
	(
		p_cron_id,
		p_user_id,
		p_cron_tab,
		nvl(c_user, user),
		systimestamp
	);

	dgcrontab_makelines(
		c_user=>c_user,
		p_cron_id=>p_cron_id,
		p_cron_tab=>p_cron_tab
	);
end;

/


create or replace procedure DGHOST_INSERT
(
	c_user in varchar2,
	p_host_id in out integer,
	p_host_name in varchar2 := null,
	p_host_fqdn in varchar2 := null,
	p_host_ip in varchar2 := null,
	p_host_sysname in varchar2 := null,
	p_host_nodename in varchar2 := null,
	p_host_release in varchar2 := null,
	p_host_version in varchar2 := null,
	p_host_machine in varchar2 := null
)
as
begin
	if p_host_id is null then
		select seq_dghost.nextval into p_host_id from dual;
	end if;

	insert into dghost
	(
		host_id,
		host_name,
		host_fqdn,
		host_ip,
		host_sysname,
		host_nodename,
		host_release,
		host_version,
		host_machine,
		host_cname,
		host_cdate
	)
	values
	(
		p_host_id,
		p_host_name,
		p_host_fqdn,
		p_host_ip,
		p_host_sysname,
		p_host_nodename,
		p_host_release,
		p_host_version,
		p_host_machine,
		nvl(c_user, user),
		systimestamp
	);
end;

/


create or replace procedure DGJOB_INSERT
(
	c_user in varchar2,
	p_job_id in out integer,
	p_pro_id in integer := null,
	p_job_name in varchar2 := null,
	p_job_active in integer := 1,
	p_job_overwritescriptconfig in integer := 0,
	p_job_logfilename in varchar2 := null,
	p_job_loglinkname in varchar2 := null,
	p_job_pidfilename in varchar2 := null,
	p_job_log2file in integer := null,
	p_job_log2db in integer := null,
	p_job_formatlogline in varchar2 := null,
	p_job_keepfilelogs in integer := null,
	p_job_keepdblogs in integer := null,
	p_job_keepdbruns in integer := null
)
as
	v_dgparameter dgparameter%rowtype;
begin
	if p_job_id is null then
		select seq_dgjob.nextval into p_job_id from dual;
	end if;

	select * into v_dgparameter from dgparameter;

	insert into dgjob
	(
		job_id,
		pro_id,
		job_name,
		job_active,
		job_overwritescriptconfig,
		job_log2file,
		job_log2db,
		job_logfilename,
		job_loglinkname,
		job_pidfilename,
		job_formatlogline,
		job_keepfilelogs,
		job_keepdblogs,
		job_keepdbruns,
		job_cname,
		job_cdate
	)
	values
	(
		p_job_id,
		p_pro_id,
		p_job_name,
		p_job_active,
		p_job_overwritescriptconfig,
		decode(p_job_log2file, v_dgparameter.par_log2file, null, p_job_log2file),
		decode(p_job_log2db, v_dgparameter.par_log2db, null, p_job_log2db),
		decode(p_job_logfilename, v_dgparameter.par_logfilename, null, p_job_logfilename),
		decode(p_job_loglinkname, v_dgparameter.par_loglinkname, null, p_job_loglinkname),
		decode(p_job_pidfilename, v_dgparameter.par_pidfilename, null, p_job_pidfilename),
		decode(p_job_formatlogline, v_dgparameter.par_formatlogline, null, p_job_formatlogline),
		decode(p_job_keepfilelogs, v_dgparameter.par_keepfilelogs, null, p_job_keepfilelogs),
		decode(p_job_keepdblogs, v_dgparameter.par_keepdblogs, null, p_job_keepdblogs),
		decode(p_job_keepdbruns, v_dgparameter.par_keepdbruns, null, p_job_keepdbruns),
		nvl(c_user, user),
		systimestamp
	);
end;

/


create or replace procedure DGPARAMETER_INSERT
(
	c_user in varchar2,
	c_message out varchar2,
	p_par_id in out integer,
	p_par_active in integer := null,
	p_par_log2file in integer := null,
	p_par_log2db in integer := null,
	p_par_logfilename in varchar2 := null,
	p_par_loglinkname in varchar2 := null,
	p_par_pidfilename in varchar2 := null,
	p_par_formatlogline in varchar2 := null,
	p_par_keepfilelogs in integer := null,
	p_par_keepdblogs in integer := null,
	p_par_keepdbruns in integer := null
)
as
begin
	if p_par_id is null then
		select seq_dgparameter.nextval into p_par_id from dual;
	end if;

	insert into dgparameter
	(
		par_id,
		par_active,
		par_log2file,
		par_log2db,
		par_logfilename,
		par_loglinkname,
		par_pidfilename,
		par_formatlogline,
		par_keepfilelogs,
		par_keepdblogs,
		par_keepdbruns,
		par_cname,
		par_cdate
	)
	values
	(
		p_par_id,
		p_par_active,
		p_par_log2file,
		p_par_log2db,
		p_par_logfilename,
		p_par_loglinkname,
		p_par_pidfilename,
		p_par_formatlogline,
		p_par_keepfilelogs,
		p_par_keepdblogs,
		p_par_keepdbruns,
		nvl(c_user, user),
		systimestamp
	);
	c_message := 'Parameter gespeichert';
end;

/


create or replace procedure DGPROJECT_INSERT
(
	c_user in varchar2,
	p_pro_id in out integer,
	p_pro_name in varchar2 := null
)
as
begin
	if p_pro_id is null then
		select seq_dgproject.nextval into p_pro_id from dual;
	end if;

	insert into dgproject
	(
		pro_id,
		pro_name,
		pro_cname,
		pro_cdate
	)
	values
	(
		p_pro_id,
		p_pro_name,
		nvl(c_user, user),
		systimestamp
	);
end;

/


create or replace procedure DGRUN_START
(
	c_user in varchar2,
	p_run_id in out integer,
	p_pro_name in varchar2 := null,
	p_job_name in varchar2 := null,
	p_host_name in varchar2 := null,
	p_host_fqdn in varchar2 := null,
	p_host_ip in varchar2 := null,
	p_host_sysname in varchar2 := null,
	p_host_nodename in varchar2 := null,
	p_host_release in varchar2 := null,
	p_host_version in varchar2 := null,
	p_host_machine in varchar2 := null,
	p_user_name in varchar2 := null,
	p_user_uid in integer := null,
	p_user_gid in integer := null,
	p_user_gecos in varchar2 := null,
	p_user_dir in varchar2 := null,
	p_user_shell in varchar2 := null,
	p_scr_filename in varchar2 := null,
	p_scr_source in clob := null,
	p_cron_tab in clob := null,
	p_run_start in timestamp := null,
	p_run_pid in integer := null,
	p_job_log2file in out integer,
	p_job_log2db in out integer,
	p_job_logfilename in out varchar2,
	p_job_loglinkname in out varchar2,
	p_job_pidfilename in out varchar2,
	p_job_formatlogline in out varchar2,
	p_job_keepfilelogs in out integer,
	p_job_keepdblogs in out integer,
	p_job_keepdbruns in out integer,
	p_job_active out integer
)
as
	v_pro_id integer;
	v_job_id integer;
	v_host_id integer;
	v_user_id integer;
	v_scr_id integer;
	v_cron_id integer;
	v_found integer;
	v_scr_filename dgscript.scr_filename%type;
	v_scr_source clob;
	v_cron_tab clob;
	v_par_id integer;
	v_message varchar2(4000);
	v_job_active dgjob.job_active%type;
	v_job_overwritescriptconfig integer;
	v_job_log2file dgjob.job_log2file%type;
	v_job_log2db dgjob.job_log2db%type;
	v_job_logfilename dgjob.job_logfilename%type;
	v_job_loglinkname dgjob.job_loglinkname%type;
	v_job_pidfilename dgjob.job_pidfilename%type;
	v_job_formatlogline dgjob.job_formatlogline%type;
	v_job_keepfilelogs dgjob.job_keepfilelogs%type;
	v_job_keepdblogs dgjob.job_keepdblogs%type;
	v_job_keepdbruns dgjob.job_keepdbruns%type;
begin
	-- Create global parameter record if none exists
	select count(*) into v_found from dgparameter;
	if v_found = 0 then
		dgparameter_insert(
			c_user=>c_user,
			c_message=>v_message,
			p_par_id=>v_par_id,
			p_par_active=>1,
			p_par_log2file=>1,
			p_par_log2db=>1,
			p_par_logfilename=>'~<?print user_name?>/log/<?print projectname?>/<?print jobname?>/<?print starttime.format(''%Y-%m-%d-%H-%M-%S-%f'')?>.sisyphuslog',
			p_par_loglinkname=>'~<?print user_name?>/log/<?print projectname?>/<?print jobname?>/current.sisyphuslog',
			p_par_pidfilename=>'~<?print user_name?>/run/<?print projectname?>/<?print jobname?>.pid',
			p_par_formatlogline=>'[<?print time?>]=[t+<?print time-starttime?>]<?if tags?>[<?print '', ''.join(tags)?>]<?end if?>: <?print line?>\n',
			p_par_keepfilelogs=>30,
			p_par_keepdblogs=>90,
			p_par_keepdbruns=>300
		);
	end if;

	-- Create the project
	begin
		select pro_id into v_pro_id from dgproject where pro_name = p_pro_name;
	exception when no_data_found then
		dgproject_insert(c_user=>c_user, p_pro_id=>v_pro_id, p_pro_name=>p_pro_name);
	end;

	-- Create the job
	begin
		select
			j.job_id,
			least(j.job_active, p_job_active),
			j.job_overwritescriptconfig,
			nvl(j.job_log2file, p.par_log2file),
			nvl(j.job_log2db, p.par_log2db),
			nvl(j.job_logfilename, p.par_logfilename),
			nvl(j.job_loglinkname, p.par_loglinkname),
			nvl(j.job_pidfilename, p.par_pidfilename),
			nvl(j.job_formatlogline, p.par_formatlogline),
			nvl(j.job_keepfilelogs, p.par_keepfilelogs),
			nvl(j.job_keepdblogs, p.par_keepdblogs),
			nvl(j.job_keepdbruns, p.par_keepdbruns)
		into
			v_job_id,
			v_job_active,
			v_job_overwritescriptconfig,
			v_job_log2file,
			v_job_log2db,
			v_job_logfilename,
			v_job_loglinkname,
			v_job_pidfilename,
			v_job_formatlogline,
			v_job_keepfilelogs,
			v_job_keepdblogs,
			v_job_keepdbruns
		from
			dgjob j, dgparameter p
		where
			j.pro_id = v_pro_id and
			j.job_name = p_job_name;
	exception when no_data_found then
		p_job_active := 1;
		v_job_overwritescriptconfig := 0;
		v_job_log2file := p_job_log2file;
		v_job_log2db := p_job_log2db;
		v_job_logfilename := p_job_logfilename;
		v_job_loglinkname := p_job_loglinkname;
		v_job_pidfilename := p_job_pidfilename;
		v_job_formatlogline := p_job_formatlogline;
		v_job_keepfilelogs := p_job_keepfilelogs;
		v_job_keepdblogs := p_job_keepdblogs;
		v_job_keepdbruns := p_job_keepdbruns;
		dgjob_insert(
			c_user=>c_user,
			p_job_id=>v_job_id,
			p_pro_id=>v_pro_id,
			p_job_name=>p_job_name,
			p_job_active=>p_job_active,
			p_job_overwritescriptconfig=>v_job_overwritescriptconfig,
			p_job_log2file=>v_job_log2file,
			p_job_log2db=>v_job_log2db,
			p_job_logfilename=>v_job_logfilename,
			p_job_loglinkname=>v_job_loglinkname,
			p_job_pidfilename=>v_job_pidfilename,
			p_job_formatlogline=>v_job_formatlogline,
			p_job_keepfilelogs=>v_job_keepfilelogs,
			p_job_keepdblogs=>v_job_keepdblogs,
			p_job_keepdbruns=>v_job_keepdbruns
		);
	end;

	-- If we overwrite the script config with the db config, set the relevant out parameters
	if v_job_overwritescriptconfig != 0 then
		p_job_log2file := v_job_log2file;
		p_job_log2db := v_job_log2db;
		p_job_logfilename := v_job_logfilename;
		p_job_loglinkname := v_job_loglinkname;
		p_job_pidfilename := v_job_pidfilename;
		p_job_formatlogline := v_job_formatlogline;
		p_job_keepfilelogs := v_job_keepfilelogs;
		p_job_keepdblogs := v_job_keepdblogs;
		p_job_keepdbruns := v_job_keepdbruns;
	end if;

	p_job_active := v_job_active;

	-- Create the host
	begin
		v_found := 0;
		select host_id into v_host_id from dghost where host_ip = p_host_ip;
		v_found := 1;
	exception when no_data_found then
		dghost_insert(
			c_user=>c_user,
			p_host_id=>v_host_id,
			p_host_name=>p_host_name,
			p_host_fqdn=>p_host_fqdn,
			p_host_ip=>p_host_ip,
			p_host_sysname=>p_host_sysname,
			p_host_nodename=>p_host_nodename,
			p_host_release=>p_host_release,
			p_host_version=>p_host_version,
			p_host_machine=>p_host_machine
		);
	end;
	if v_found = 1 then
		update
			dghost
		set
			host_name = p_host_name,
			host_fqdn = p_host_fqdn,
			host_ip = p_host_ip,
			host_sysname = p_host_sysname,
			host_nodename = p_host_nodename,
			host_release = p_host_release,
			host_version = p_host_version,
			host_machine = p_host_machine,
			host_uname = nvl(c_user, user),
			host_udate = systimestamp
		where
			host_id = v_host_id and
			( -- only update if any of the fields has changed
				host_name != p_host_name or
				host_fqdn != p_host_fqdn or
				host_sysname != p_host_sysname or
				host_nodename != p_host_nodename or
				host_release != p_host_release or
				host_version != p_host_version or
				host_machine != p_host_machine
			)
		;
	end if;

	-- Create the user
	begin
		v_found := 0;
		select user_id into v_user_id from dguser where host_id = v_host_id and user_name = p_user_name;
		v_found := 1;
	exception when no_data_found then
		dguser_insert(
			c_user=>c_user,
			p_user_id=>v_user_id,
			p_host_id=>v_host_id,
			p_user_name=>p_user_name,
			p_user_uid=>p_user_uid,
			p_user_gid=>p_user_gid,
			p_user_gecos=>p_user_gecos,
			p_user_dir=>p_user_dir,
			p_user_shell=>p_user_shell
		);
	end;
	if v_found = 1 then
		update
			dguser
		set
			user_uid = p_user_uid,
			user_gid = p_user_gid,
			user_gecos = p_user_gecos,
			user_dir = p_user_dir,
			user_shell = p_user_shell,
			user_uname = nvl(c_user, user),
			user_udate = systimestamp
		where
			user_id = v_user_id and
			( -- only update if any of the fields has changed
				user_uid != p_user_uid or
				user_gid != p_user_gid or
				user_gecos != p_user_gecos or
				user_dir != p_user_dir or
				user_shell != p_user_shell
			);
	end if;

	if p_job_log2db != 0 then
		-- Find the current script source
		v_scr_id := null;
		for row in (select /*+ FIRST_ROWS(1)*/ scr_id, scr_filename, scr_source from dgscript where job_id = v_job_id order by scr_cdate desc) loop
			v_scr_id := row.scr_id;
			v_scr_filename := row.scr_filename;
			v_scr_source := row.scr_source;
			exit;
		end loop;

		-- Script has changed or is new
		if v_scr_id is null or dbms_lob.compare(p_scr_source, v_scr_source) != 0 or p_scr_filename != v_scr_filename then
			v_scr_id := null;
			dgscript_insert(
				c_user=>c_user,
				p_scr_id=>v_scr_id,
				p_job_id=>v_job_id,
				p_scr_filename=>p_scr_filename,
				p_scr_source=>p_scr_source
			);
		end if;

		-- Find the current crontab
		v_cron_id := null;
		for row in (select /*+ FIRST_ROWS(1)*/ cron_id, cron_tab from dgcrontab where user_id = v_user_id order by cron_cdate desc) loop
			v_cron_id := row.cron_id;
			v_cron_tab := row.cron_tab;
			exit;
		end loop;

		-- Crontab has changed or is new
		if v_cron_id is null or dbms_lob.compare(p_cron_tab, v_cron_tab) != 0 then
			v_cron_id := null;
			dgcrontab_insert(
				c_user=>c_user,
				p_cron_id=>v_cron_id,
				p_user_id=>v_user_id,
				p_cron_tab=>p_cron_tab
			);
		end if;

		if p_run_id is null then
			select seq_dgrun.nextval into p_run_id from dual;
		end if;

		insert into dgrun
		(
			run_id,
			job_id,
			user_id,
			run_pid,
			run_start,
			run_end,
			run_errors,
			run_ok,
			run_result,
			scr_id,
			cron_id,
			run_cname,
			run_cdate
		)
		values
		(
			p_run_id,
			v_job_id,
			v_user_id,
			p_run_pid,
			p_run_start, -- start now
			null, -- still running
			0, -- no errors logged yet
			null, -- ok/failed not determined yet
			null, -- no result
			v_scr_id,
			v_cron_id,
			nvl(c_user, user),
			systimestamp
		);
	end if;
end;

/


create or replace procedure DGLOGLINE_INSERT
(
	c_user in varchar2,
	p_log_id in out integer,
	p_run_id in integer := null,
	p_log_lineno in integer := null,
	p_log_date in timestamp := null,
	p_log_tags in varchar2 := null,
	p_log_line in clob := null
)
as
begin
	if p_log_id is null then
		select seq_dglogline.nextval into p_log_id from dual;
	end if;

	insert into dglogline
	(
		log_id,
		run_id,
		log_lineno,
		log_date,
		log_tags,
		log_line,
		log_cname,
		log_cdate
	)
	values
	(
		p_log_id,
		p_run_id,
		p_log_lineno,
		p_log_date,
		p_log_tags,
		p_log_line,
		nvl(c_user, user),
		systimestamp
	);
end;

/


create or replace procedure DGRUN_LOG
(
	c_user in varchar2,
	p_run_id in integer,
	p_log_lineno in integer := null,
	p_log_date in timestamp := null,
	p_log_tags in varchar2 := null,
	p_log_line in clob := null
)
as
	v_log_id integer;
begin
	dglogline_insert
	(
		c_user=>c_user,
		p_log_id=>v_log_id,
		p_run_id=>p_run_id,
		p_log_lineno=>p_log_lineno,
		p_log_date=>p_log_date,
		p_log_tags=>p_log_tags,
		p_log_line=>p_log_line
	);
end;

/


create or replace procedure DGRUN_INSERT
(
	c_user in varchar2,
	p_run_id in out integer,
	p_job_id in integer := null,
	p_user_id in integer := null,
	p_run_pid in integer := null,
	p_run_start in timestamp := null,
	p_run_end in timestamp := null,
	p_run_errors in integer := null,
	p_run_ok in integer := null,
	p_run_result in varchar2 := null,
	p_scr_id in integer := null,
	p_cron_id in integer := null
)
as
begin
	if p_run_id is null then
		select seq_dgrun.nextval into p_run_id from dual;
	end if;

	insert into dgrun
	(
		run_id,
		job_id,
		user_id,
		run_pid,
		run_start,
		run_end,
		run_errors,
		run_ok,
		run_result,
		scr_id,
		cron_id,
		run_cname,
		run_cdate
	)
	values
	(
		p_run_id,
		p_job_id,
		p_user_id,
		p_run_pid,
		p_run_start,
		p_run_end,
		p_run_errors,
		p_run_ok,
		p_run_result,
		p_scr_id,
		p_cron_id,
		nvl(c_user, user),
		systimestamp
	);
end;

/


create or replace procedure DGRUN_CLEANUP
(
	c_user in varchar2,
	p_keepdblogs in integer,
	p_keepdbruns in integer
)
as
	v_now timestamp;
begin
	v_now := systimestamp;

	delete from dglogline where log_date < v_now - p_keepdblogs or log_date < v_now - p_keepdbruns;
	delete from dgrun where run_start < v_now - p_keepdbruns;
end;

/


create or replace procedure DGRUN_FAILED
(
	c_user in varchar2,
	p_run_id in integer,
	p_run_end in timestamp := null,
	p_run_result in varchar2 := null,
	p_keepdblogs in integer := null,
	p_keepdbruns in integer := null
)
as
begin
	update dgrun set
		run_end = p_run_end,
		run_ok = 0,
		run_result = p_run_result,
		run_uname = nvl(c_user, user),
		run_udate = systimestamp
	where
		run_id = p_run_id;

	dgrun_cleanup(c_user=>c_user, p_keepdblogs=>p_keepdblogs, p_keepdbruns=>p_keepdbruns);
end;

/


create or replace procedure DGRUN_ERROR
(
	c_user in varchar2,
	p_run_id in integer
)
as
begin
	update dgrun set
		run_errors = run_errors + 1,
		run_uname = nvl(c_user, user),
		run_udate = systimestamp
	where
		run_id = p_run_id;
end;

/


create or replace procedure DGRUN_END
(
	c_user in varchar2,
	p_run_id in integer,
	p_run_end in timestamp := null,
	p_run_result in varchar2 := null,
	p_keepdblogs in integer := null,
	p_keepdbruns in integer := null
)
as
begin
	update dgrun set
		run_end = p_run_end,
		run_ok = 1,
		run_result = p_run_result,
		run_uname = nvl(c_user, user),
		run_udate = systimestamp
	where
		run_id = p_run_id;

	dgrun_cleanup(c_user=>c_user, p_keepdblogs=>p_keepdblogs, p_keepdbruns=>p_keepdbruns);
end;

/


create or replace procedure DGPROJECT_UPDATE
(
	c_user in varchar2,
	p_pro_id in out integer,
	p_pro_name in varchar2 := null
)
as
begin

	update dgproject set
		pro_name = p_pro_name,
		pro_uname = nvl(c_user, user),
		pro_udate = systimestamp
	where
		pro_id = p_pro_id;
end;

/


create or replace procedure DGPROJECT_DELETE
(
	c_user in varchar2,
	p_pro_id in integer
)
as
begin
	delete from dgproject where pro_id = p_pro_id;
end;

/


create or replace procedure DGPARAMETER_UPDATE
(
	c_user in varchar2,
	c_message out varchar2,
	p_par_id in out integer,
	p_par_active in integer := null,
	p_par_log2file in integer := null,
	p_par_log2db in integer := null,
	p_par_logfilename in varchar2 := null,
	p_par_loglinkname in varchar2 := null,
	p_par_pidfilename in varchar2 := null,
	p_par_formatlogline in varchar2 := null,
	p_par_keepfilelogs in integer := null,
	p_par_keepdblogs in integer := null,
	p_par_keepdbruns in integer := null
)
as
begin

	update dgparameter set
		par_active = p_par_active,
		par_log2file = p_par_log2file,
		par_log2db = p_par_log2db,
		par_logfilename = p_par_logfilename,
		par_loglinkname = p_par_loglinkname,
		par_pidfilename = p_par_pidfilename,
		par_formatlogline = p_par_formatlogline,
		par_keepfilelogs = p_par_keepfilelogs,
		par_keepdblogs = p_par_keepdblogs,
		par_keepdbruns = p_par_keepdbruns,
		par_uname = nvl(c_user, user),
		par_udate = systimestamp
	where
		par_id = p_par_id;
	c_message := 'Parameter gespeichert';
end;

/


create or replace procedure DGPARAMETER_DELETE
(
	c_user in varchar2,
	c_message out varchar2,
	p_par_id in integer
)
as
begin
	delete from dgparameter where par_id = p_par_id;
	c_message := 'Parameter gelöscht';
end;

/


create or replace procedure DGLOGLINE_UPDATE
(
	c_user in varchar2,
	p_log_id in out integer,
	p_run_id in integer := null,
	p_log_lineno in integer := null,
	p_log_date in timestamp := null,
	p_log_tags in varchar2 := null,
	p_log_line in clob := null
)
as
begin

	update dglogline set
		run_id = p_run_id,
		log_lineno = p_log_lineno,
		log_date = p_log_date,
		log_tags = p_log_tags,
		log_line = p_log_line
	where
		log_id = p_log_id;
end;

/


create or replace procedure DGJOB_UPDATE
(
	c_user in varchar2,
	p_job_id in out integer,
	p_pro_id in integer := null,
	p_job_name in varchar2 := null,
	p_job_active in integer := 1,
	p_job_overwritescriptconfig in integer := 0,
	p_job_logfilename in varchar2 := null,
	p_job_loglinkname in varchar2 := null,
	p_job_pidfilename in varchar2 := null,
	p_job_log2file in integer := null,
	p_job_log2db in integer := null,
	p_job_formatlogline in varchar2 := null,
	p_job_keepfilelogs in integer := null,
	p_job_keepdblogs in integer := null,
	p_job_keepdbruns in integer := null
)
as
	v_dgparameter dgparameter%rowtype;
begin
	select * into v_dgparameter from dgparameter;

	update dgjob set
		pro_id = p_pro_id,
		job_name = p_job_name,
		job_active = p_job_active,
		job_overwritescriptconfig = p_job_overwritescriptconfig,
		job_log2file = decode(p_job_log2file, v_dgparameter.par_log2file, null, p_job_log2file),
		job_log2db = decode(p_job_log2db, v_dgparameter.par_log2db, null, p_job_log2db),
		job_logfilename = decode(p_job_logfilename, v_dgparameter.par_logfilename, null, p_job_logfilename),
		job_loglinkname = decode(p_job_loglinkname, v_dgparameter.par_loglinkname, null, p_job_loglinkname),
		job_pidfilename = decode(p_job_pidfilename, v_dgparameter.par_pidfilename, null, p_job_pidfilename),
		job_formatlogline = decode(p_job_formatlogline, v_dgparameter.par_formatlogline, null, p_job_formatlogline),
		job_keepfilelogs = decode(p_job_keepfilelogs, v_dgparameter.par_keepfilelogs, null, p_job_keepfilelogs),
		job_keepdblogs = decode(p_job_keepdblogs, v_dgparameter.par_keepdblogs, null, p_job_keepdblogs),
		job_keepdbruns = decode(p_job_keepdbruns, v_dgparameter.par_keepdbruns, null, p_job_keepdbruns),
		job_uname = nvl(c_user, user),
		job_udate = systimestamp
	where
		job_id = p_job_id;
end;

/


create or replace procedure DGJOB_DELETE
(
	c_user in varchar2,
	p_job_id in integer
)
as
begin
	for row in (select run_id from dgrun where job_id=p_job_id) loop
		dgrun_delete(c_user, row.run_id);
	end loop;

	for row in (select scr_id from dgscript where job_id=p_job_id) loop
		dgscript_delete(c_user, row.scr_id);
	end loop;

	delete from dgjob where job_id = p_job_id;
end;

/


create or replace procedure DGHOST_UPDATE
(
	c_user in varchar2,
	p_host_id in out integer,
	p_host_name in varchar2 := null,
	p_host_fqdn in varchar2 := null,
	p_host_ip in varchar2 := null,
	p_host_sysname in varchar2 := null,
	p_host_nodename in varchar2 := null,
	p_host_release in varchar2 := null,
	p_host_version in varchar2 := null,
	p_host_machine in varchar2 := null
)
as
begin

	update dghost set
		host_name = p_host_name,
		host_fqdn = p_host_fqdn,
		host_ip = p_host_ip,
		host_sysname = p_host_sysname,
		host_nodename = p_host_nodename,
		host_release = p_host_release,
		host_version = p_host_version,
		host_machine = p_host_machine,
		host_uname = nvl(c_user, user),
		host_udate = systimestamp
	where
		host_id = p_host_id;
end;

/


create or replace procedure DGHOST_DELETE
(
	c_user in varchar2,
	p_host_id in integer
)
as
begin
	delete from dghost where host_id = p_host_id;
end;

/


create or replace procedure DGCRONTABLINE_DELETE
(
	c_user in varchar2,
	p_ctl_id in integer
)
as
begin
	delete from dgcrontabline where ctl_id = p_ctl_id;
end;

/


create or replace procedure DGCRONTAB_DELETE
(
	c_user in varchar2,
	p_cron_id in integer
)
as
begin
	for row in (select ctl_id from dgcrontabline where cron_id=p_cron_id) loop
		dgcrontabline_delete(c_user, row.ctl_id);
	end loop;

	delete from dgcrontab where cron_id = p_cron_id;
end;

/


create or replace procedure DGCRONTABLINE_UPDATE
(
	c_user in varchar2,
	p_ctl_id in out integer,
	p_cron_id in integer := null,
	p_ctl_lineno in integer := null,
	p_ctl_type in integer := null,
	p_ctl_minute in varchar2 := null,
	p_ctl_hour in varchar2 := null,
	p_ctl_dayofmonth in varchar2 := null,
	p_ctl_month in varchar2 := null,
	p_ctl_dayofweek in varchar2 := null,
	p_ctl_line in varchar2 := null
)
as
begin

	update dgcrontabline set
		cron_id = p_cron_id,
		ctl_lineno = p_ctl_lineno,
		ctl_type = p_ctl_type,
		ctl_minute = p_ctl_minute,
		ctl_hour = p_ctl_hour,
		ctl_dayofmonth = p_ctl_dayofmonth,
		ctl_month = p_ctl_month,
		ctl_dayofweek = p_ctl_dayofweek,
		ctl_line = p_ctl_line
	where
		ctl_id = p_ctl_id;
end;

/


