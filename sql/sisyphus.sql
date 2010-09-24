create sequence seq_dgparameter
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence seq_dghost
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence seq_dguser
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence seq_dgproject
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence seq_dgjob
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence seq_dgrun
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence seq_dglogline
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence seq_dgscript
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create sequence seq_dgcrontab
	increment by 10
	start with 10
	maxvalue 9999999999999999999999999999
	minvalue 10
	nocycle
	cache 20
	noorder;


create table dgparameter
(
	par_id integer not null,
	par_active integer not null,
	par_log2file integer not null,
	par_log2db integer not null,
	par_logfilename varchar2(1024 byte) not null,
	par_loglinkname varchar2(1024 byte),
	par_pidfilename varchar2(1024 byte) not null,
	par_formatlogline varchar2(1024 byte) not null,
	par_keepfilelogs integer not null,
	par_keepdblogs integer not null,
	par_keebdbruns integer,
	par_cname varchar2(64 byte),
	par_cdate timestamp(6) with time zone,
	par_uname varchar2(64 byte),
	par_udate timestamp(6) with time zone
);


alter table dgparameter add constraint pk_dgparameter primary key(par_id);


comment on column dgparameter.par_id is '';


comment on column dgparameter.par_active is '';


comment on column dgparameter.par_log2file is '';


comment on column dgparameter.par_log2db is '';


comment on column dgparameter.par_logfilename is '';


comment on column dgparameter.par_loglinkname is '';


comment on column dgparameter.par_pidfilename is '';


comment on column dgparameter.par_formatlogline is '';


comment on column dgparameter.par_keepfilelogs is '';


comment on column dgparameter.par_keepdblogs is '';


comment on column dgparameter.par_keebdbruns is '';


comment on column dgparameter.par_cname is '';


comment on column dgparameter.par_cdate is '';


comment on column dgparameter.par_uname is '';


comment on column dgparameter.par_udate is '';


create table dghost
(
	host_id integer not null,
	host_name varchar2(256 byte) not null,
	host_fqdn varchar2(256 byte) not null,
	host_ip varchar2(256 byte) not null,
	host_sysname varchar2(256 byte),
	host_nodename varchar2(256 byte),
	host_release varchar2(256 byte),
	host_version varchar2(256 byte),
	host_machine varchar2(256 byte),
	host_cname varchar2(64 byte),
	host_cdate timestamp(6) with time zone,
	host_uname varchar2(64 byte),
	host_udate timestamp(6) with time zone
);


alter table dghost add constraint pk_dghost primary key(host_id);


comment on column dghost.host_id is '';


comment on column dghost.host_name is '';


comment on column dghost.host_fqdn is '';


comment on column dghost.host_ip is '';


comment on column dghost.host_sysname is '';


comment on column dghost.host_nodename is '';


comment on column dghost.host_release is '';


comment on column dghost.host_version is '';


comment on column dghost.host_machine is '';


comment on column dghost.host_cname is '';


comment on column dghost.host_cdate is '';


comment on column dghost.host_uname is '';


comment on column dghost.host_udate is '';


create table dguser
(
	user_id integer not null,
	host_id integer not null,
	user_name varchar2(256 byte) not null,
	user_uid integer,
	user_gid integer,
	user_gecos varchar2(256 byte),
	user_dir varchar2(256 byte),
	user_shell varchar2(256 byte),
	user_cname varchar2(64 byte),
	user_cdate timestamp(6) with time zone,
	user_uname varchar2(64 byte),
	user_udate timestamp(6) with time zone
);


alter table dguser add constraint pk_dguser primary key(user_id);


comment on column dguser.user_id is '';


comment on column dguser.host_id is '';


comment on column dguser.user_name is '';


comment on column dguser.user_uid is '';


comment on column dguser.user_gid is '';


comment on column dguser.user_gecos is '';


comment on column dguser.user_dir is '';


comment on column dguser.user_shell is '';


comment on column dguser.user_cname is '';


comment on column dguser.user_cdate is '';


comment on column dguser.user_uname is '';


comment on column dguser.user_udate is '';


create table dgproject
(
	pro_id integer not null,
	pro_name varchar2(256 byte) not null,
	pro_cname varchar2(64 byte),
	pro_cdate timestamp(6) with time zone,
	pro_uname varchar2(64 byte),
	pro_udate timestamp(6) with time zone
);


alter table dgproject add constraint pk_dgproject primary key(pro_id);


comment on column dgproject.pro_id is '';


comment on column dgproject.pro_name is '';


comment on column dgproject.pro_cname is '';


comment on column dgproject.pro_cdate is '';


comment on column dgproject.pro_uname is '';


comment on column dgproject.pro_udate is '';


create table dgscript
(
	scr_id integer not null,
	job_id integer not null,
	scr_filename varchar2(1024 byte) not null,
	scr_source clob,
	scr_cname varchar2(64 byte),
	scr_cdate timestamp(6) with time zone
);


alter table dgscript add constraint pk_dgscript primary key(scr_id);


comment on column dgscript.scr_id is '';


comment on column dgscript.job_id is '';


comment on column dgscript.scr_filename is '';


comment on column dgscript.scr_source is '';


comment on column dgscript.scr_cname is '';


comment on column dgscript.scr_cdate is '';


create table dgrun
(
	run_id integer not null,
	job_id integer not null,
	user_id integer not null,
	run_pid integer not null,
	run_start timestamp(6),
	run_end timestamp(6),
	run_errors integer not null,
	run_ok integer,
	run_result varchar2(1024 byte),
	scr_id integer not null,
	cron_id integer not null,
	run_cname varchar2(64 byte),
	run_cdate timestamp(6) with time zone,
	run_uname varchar2(64 byte),
	run_udate timestamp(6) with time zone
);


alter table dgrun add constraint pk_dgrun primary key(run_id);


comment on column dgrun.run_id is '';


comment on column dgrun.job_id is '';


comment on column dgrun.user_id is '';


comment on column dgrun.run_pid is '';


comment on column dgrun.run_start is '';


comment on column dgrun.run_end is '';


comment on column dgrun.run_errors is '';


comment on column dgrun.run_ok is '';


comment on column dgrun.run_result is '';


comment on column dgrun.scr_id is '';


comment on column dgrun.cron_id is '';


comment on column dgrun.run_cname is '';


comment on column dgrun.run_cdate is '';


comment on column dgrun.run_uname is '';


comment on column dgrun.run_udate is '';


create table dgjob
(
	job_id integer not null,
	pro_id integer not null,
	job_name varchar2(256 byte) not null,
	job_active integer default 1  not null,
	job_logfilename varchar2(1024 byte),
	job_loglinkname varchar2(1024 byte),
	job_pidfilename varchar2(1024 byte),
	job_log2file integer,
	job_log2db integer,
	job_formatlogline varchar2(256 byte),
	par_keepfilelogs integer,
	par_keepdblogs integer,
	par_keebdbruns integer,
	job_cname varchar2(64 byte),
	job_cdate timestamp(6) with time zone,
	job_uname varchar2(64 byte),
	job_udate timestamp(6) with time zone
);


alter table dgjob add constraint pk_dgjob primary key(job_id);


comment on column dgjob.job_id is '';


comment on column dgjob.pro_id is '';


comment on column dgjob.job_name is '';


comment on column dgjob.job_active is '';


comment on column dgjob.job_logfilename is '';


comment on column dgjob.job_loglinkname is '';


comment on column dgjob.job_pidfilename is '';


comment on column dgjob.job_log2file is '';


comment on column dgjob.job_log2db is '';


comment on column dgjob.job_formatlogline is '';


comment on column dgjob.par_keepfilelogs is '';


comment on column dgjob.par_keepdblogs is '';


comment on column dgjob.par_keebdbruns is '';


comment on column dgjob.job_cname is '';


comment on column dgjob.job_cdate is '';


comment on column dgjob.job_uname is '';


comment on column dgjob.job_udate is '';


create table dgcrontab
(
	cron_id integer not null,
	user_id integer not null,
	cron_tab clob,
	cron_cname varchar2(64 byte),
	cron_cdate timestamp(6) with time zone
);


alter table dgcrontab add constraint pk_dgcrontab primary key(cron_id);


comment on column dgcrontab.cron_id is '';


comment on column dgcrontab.user_id is '';


comment on column dgcrontab.cron_tab is '';


comment on column dgcrontab.cron_cname is '';


comment on column dgcrontab.cron_cdate is '';


create table dglogline
(
	log_id integer not null,
	run_id integer not null,
	log_lineno integer,
	log_date timestamp(6),
	log_tags varchar2(256 byte),
	log_line clob,
	log_cname varchar2(64 byte),
	log_cdate timestamp(6) with time zone
);


alter table dglogline add constraint pk_dglogline primary key(log_id);


comment on column dglogline.log_id is '';


comment on column dglogline.run_id is '';


comment on column dglogline.log_lineno is '';


comment on column dglogline.log_date is '';


comment on column dglogline.log_tags is '';


comment on column dglogline.log_line is '';


comment on column dglogline.log_cname is '';


comment on column dglogline.log_cdate is '';


alter table dgcrontab add constraint fk1_dgcrontab foreign key (user_id) references dguser(user_id);


alter table dghost add constraint uk1_dghost unique(host_ip);


alter table dgjob add constraint uk1_dgjob unique(pro_id, job_name);


alter table dglogline add constraint fk1_dglogline foreign key (run_id) references dgrun(run_id);


alter table dgproject add constraint uk1_dgproject unique(pro_name);


alter table dgrun add constraint fk1_dgrun foreign key (job_id) references dgjob(job_id);


alter table dgrun add constraint fk2_dgrun foreign key (user_id) references dguser(user_id);


alter table dgrun add constraint fk3_dgrun foreign key (scr_id) references dgscript(scr_id);


alter table dgrun add constraint fk4_dgrun foreign key (cron_id) references dgcrontab(cron_id);


alter table dgscript add constraint fk1_dgscript foreign key (job_id) references dgjob(job_id);


alter table dguser add constraint fk1_dguser foreign key (host_id) references dghost(host_id);


alter table dguser add constraint uk1_dguser unique(host_id, user_name);


create or replace force view dgrun_select as
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


create or replace force view dgscript_select as
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


create or replace force view dglogline_select as
	select
		log_id,
		run_id,
		log_lineno,
		log_date,
		log_tags,
		log_line,
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


create or replace force view dgcrontab_select as
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


create or replace force view dgjob_select as
	select
	j.job_id,
	j.pro_id,
	p.pro_name,
	j.job_name,
	j.job_active,
	j.job_logfilename,
	j.job_loglinkname,
	j.job_pidfilename,
	j.job_log2file,
	j.job_log2db,
	j.job_formatlogline,
	j.par_keepfilelogs,
	j.par_keepdblogs,
	j.par_keebdbruns,
	j.job_cname,
	j.job_cdate,
	j.job_uname,
	j.job_udate
from
	dgjob j,
	dgproject p
where
	j.pro_id=p.pro_id
/


create or replace force view dgproject_select as
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


create or replace force view dguser_select as
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


create or replace force view dghost_select as
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


create or replace force view dgparameter_select as
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
		par_keebdbruns,
		par_cname,
		par_cdate,
		par_uname,
		par_udate
	from
		dgparameter
/


create or replace function abbrev
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


create or replace function xmlescape
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


create or replace function log_ftext
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


create or replace function log_fhtml
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
		write(replace(xmlescape(row.log_line), ' ', '&#160;'));
		write('</td></tr>');
	end loop;
	write('</table>');
	return c_out;
end;

/


create or replace function crontab_fhtml
(
	p_crontab in clob
)
return clob
as
	c_out clob;
	v_start integer;
	v_end integer;
	v_inlinestart integer;
	v_inlineend integer;
	v_line varchar2(32000);
	v_part varchar2(32000);
	v_count integer;
	v_td varchar2(2);
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
	v_end := 0;
	write('<table border="0" cellpadding="0" cellspacing="0" class="crontab">');
	if p_crontab is not null then
		loop
			v_start := v_end + 1;
			v_end := instr(p_crontab, chr(10), v_start);
			if v_end = 0 then
				v_end := length(p_crontab) + 1;
			end if;
			v_line := dbms_lob.substr(p_crontab, v_end - v_start, v_start);
			v_line := regexp_replace(v_line, '^[ \t]*', '');
			if regexp_like(v_line, '^[0-9*]') then
				v_inlineend := 0;
				write('<tr>');
				v_count := 1;
				v_td := 'th';
				loop
					v_inlinestart := v_inlineend + 1;
					v_inlineend := regexp_instr(v_line, '[ \t]+', v_inlinestart, 1, 1);
					if v_inlineend = 0 then
						v_inlineend := length(v_line) + 1;
					elsif v_count = 6 then
						v_inlineend := length(v_line) + 1;
						v_td := 'td';
					else
						v_inlineend := v_inlineend - 1;
					end if;
					v_part := substr(v_line, v_inlinestart, v_inlineend - v_inlinestart);
					v_part := regexp_replace(v_part, '[ \t]*$', '');
					write('<' || v_td || '>' || replace(xmlescape(v_part), ' ', '&#160;') || '</' || v_td || '>');
					if v_inlineend >= length(v_line) then
						exit;
					end if;
					v_count := v_count + 1;
				end loop;
				write('</tr>');
			elsif regexp_like(v_line, '^#') then
				write('<tr><td colspan="6" class="comment">' || replace(xmlescape(v_line), ' ', '&#160;') || '</td></tr>');
			else
				write('<tr><td colspan="6" class="env">' || replace(xmlescape(v_line), ' ', '&#160;') || '</td></tr>');
			end if;
			if v_end >= length(p_crontab) then
				exit;
			end if;
		end loop;
	end if;
	write('</table>');
	return c_out;
end;

/


create or replace function script_fhtml
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
			v_line := xmlescape(v_line);
			v_line := replace(v_line, ' ', '&#160;');
			v_line := replace(v_line, chr(9), '<span class="tab">&#183;&#160;&#160;</span>');
			write('<tr><th>');
			write(v_count);
			write('</th><td>');
			write(v_line);
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


create or replace procedure dgrun_end
(
	c_user in varchar2,
	p_run_id in integer,
	p_run_end in timestamp := null,
	p_run_result in varchar2 := null
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
end;

/


create or replace procedure dgrun_error
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


create or replace procedure dglogline_insert
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


create or replace procedure dglogline_update
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


create or replace procedure dglogline_delete
(
	c_user in varchar2,
	p_log_id in integer
)
as
begin
	delete from dglogline where log_id = p_log_id;
end;

/


create or replace procedure dglogline_clone
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
	select seq_dglogline.nextval into p_log_id from dual;

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


create or replace procedure dgrun_insert
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


create or replace procedure dgrun_update
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


create or replace procedure dgrun_delete
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


create or replace procedure dgrun_clone
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
	select seq_dgrun.nextval into p_run_id from dual;

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


create or replace procedure dgcrontab_insert
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
end;

/


create or replace procedure dgcrontab_update
(
	c_user in varchar2,
	p_cron_id in out integer,
	p_user_id in integer := null,
	p_cron_tab in clob := null
)
as
begin

	update dgcrontab set
		user_id = p_user_id,
		cron_tab = p_cron_tab
	where
		cron_id = p_cron_id;
end;

/


create or replace procedure dgcrontab_delete
(
	c_user in varchar2,
	p_cron_id in integer
)
as
begin
	delete from dgcrontab where cron_id = p_cron_id;
end;

/


create or replace procedure dgcrontab_clone
(
	c_user in varchar2,
	p_cron_id in out integer,
	p_user_id in integer := null,
	p_cron_tab in clob := null
)
as
begin
	select seq_dgcrontab.nextval into p_cron_id from dual;

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
end;

/


create or replace procedure dgscript_insert
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
end;

/


create or replace procedure dgscript_update
(
	c_user in varchar2,
	p_scr_id in out integer,
	p_job_id in integer := null,
	p_scr_filename in varchar2 := null,
	p_scr_source in clob := null
)
as
begin

	update dgscript set
		job_id = p_job_id,
		scr_filename = p_scr_filename,
		scr_source = p_scr_source
	where
		scr_id = p_scr_id;
end;

/


create or replace procedure dgscript_delete
(
	c_user in varchar2,
	p_scr_id in integer
)
as
begin
	delete from dgscript where scr_id = p_scr_id;
end;

/


create or replace procedure dgscript_clone
(
	c_user in varchar2,
	p_scr_id in out integer,
	p_job_id in integer := null,
	p_scr_filename in varchar2 := null,
	p_scr_source in clob := null
)
as
begin
	select seq_dgscript.nextval into p_scr_id from dual;

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
end;

/


create or replace procedure dgjob_insert
(
	c_user in varchar2,
	p_job_id in out integer,
	p_pro_id in integer := null,
	p_job_name in varchar2 := null,
	p_job_active in integer := 1,
	p_job_logfilename in varchar2 := null,
	p_job_loglinkname in varchar2 := null,
	p_job_pidfilename in varchar2 := null,
	p_job_log2file in integer := null,
	p_job_log2db in integer := null,
	p_job_formatlogline in varchar2 := null,
	p_par_keepfilelogs in integer := null,
	p_par_keepdblogs in integer := null,
	p_par_keebdbruns in integer := null
)
as
begin
	if p_job_id is null then
		select seq_dgjob.nextval into p_job_id from dual;
	end if;

	insert into dgjob
	(
		job_id,
		pro_id,
		job_name,
		job_active,
		job_logfilename,
		job_loglinkname,
		job_pidfilename,
		job_log2file,
		job_log2db,
		job_formatlogline,
		par_keepfilelogs,
		par_keepdblogs,
		par_keebdbruns,
		job_cname,
		job_cdate
	)
	values
	(
		p_job_id,
		p_pro_id,
		p_job_name,
		p_job_active,
		p_job_logfilename,
		p_job_loglinkname,
		p_job_pidfilename,
		p_job_log2file,
		p_job_log2db,
		p_job_formatlogline,
		p_par_keepfilelogs,
		p_par_keepdblogs,
		p_par_keebdbruns,
		nvl(c_user, user),
		systimestamp
	);
end;

/


create or replace procedure dgjob_update
(
	c_user in varchar2,
	p_job_id in out integer,
	p_pro_id in integer := null,
	p_job_name in varchar2 := null,
	p_job_active in integer := 1,
	p_job_logfilename in varchar2 := null,
	p_job_loglinkname in varchar2 := null,
	p_job_pidfilename in varchar2 := null,
	p_job_log2file in integer := null,
	p_job_log2db in integer := null,
	p_job_formatlogline in varchar2 := null,
	p_par_keepfilelogs in integer := null,
	p_par_keepdblogs in integer := null,
	p_par_keebdbruns in integer := null
)
as
begin
	update dgjob set
		pro_id = p_pro_id,
		job_name = p_job_name,
		job_active = p_job_active,
		job_logfilename = p_job_logfilename,
		job_loglinkname = p_job_loglinkname,
		job_pidfilename = p_job_pidfilename,
		job_log2file = p_job_log2file,
		job_log2db = p_job_log2db,
		job_formatlogline = p_job_formatlogline,
		par_keepfilelogs = p_par_keepfilelogs,
		par_keepdblogs = p_par_keepdblogs,
		par_keebdbruns = p_par_keebdbruns,
		job_uname = nvl(c_user, user),
		job_udate = systimestamp
	where
		job_id = p_job_id;
end;

/


create or replace procedure dgjob_delete
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


create or replace procedure dgjob_clone
(
	c_user in varchar2,
	p_job_id in out integer,
	p_pro_id in integer := null,
	p_job_name in varchar2 := null,
	p_job_active in integer := 1,
	p_job_logfilename in varchar2 := null,
	p_job_loglinkname in varchar2 := null,
	p_job_pidfilename in varchar2 := null,
	p_job_log2file in integer := null,
	p_job_log2db in integer := null,
	p_job_formatlogline in varchar2 := null,
	p_par_keepfilelogs in integer := null,
	p_par_keepdblogs in integer := null,
	p_par_keebdbruns in integer := null
)
as
begin
	select seq_dgjob.nextval into p_job_id from dual;

	insert into dgjob
	(
		job_id,
		pro_id,
		job_name,
		job_active,
		job_logfilename,
		job_loglinkname,
		job_pidfilename,
		job_log2file,
		job_log2db,
		job_formatlogline,
		par_keepfilelogs,
		par_keepdblogs,
		par_keebdbruns,
		job_cname,
		job_cdate
	)
	values
	(
		p_job_id,
		p_pro_id,
		p_job_name,
		p_job_active,
		p_job_logfilename,
		p_job_loglinkname,
		p_job_pidfilename,
		p_job_log2file,
		p_job_log2db,
		p_job_formatlogline,
		p_par_keepfilelogs,
		p_par_keepdblogs,
		p_par_keebdbruns,
		nvl(c_user, user),
		systimestamp
	);
end;

/


create or replace procedure dgproject_insert
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


create or replace procedure dgproject_update
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


create or replace procedure dgproject_delete
(
	c_user in varchar2,
	p_pro_id in integer
)
as
begin
	delete from dgproject where pro_id = p_pro_id;
end;

/


create or replace procedure dgproject_clone
(
	c_user in varchar2,
	p_pro_id in out integer,
	p_pro_name in varchar2 := null
)
as
begin
	select seq_dgproject.nextval into p_pro_id from dual;

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


create or replace procedure dguser_insert
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


create or replace procedure dguser_update
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


create or replace procedure dguser_delete
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


create or replace procedure dguser_clone
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
	select seq_dguser.nextval into p_user_id from dual;

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


create or replace procedure dghost_insert
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


create or replace procedure dghost_update
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


create or replace procedure dghost_delete
(
	c_user in varchar2,
	p_host_id in integer
)
as
begin
	delete from dghost where host_id = p_host_id;
end;

/


create or replace procedure dghost_clone
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
	select seq_dghost.nextval into p_host_id from dual;

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


create or replace procedure dgrun_failed
(
	c_user in varchar2,
	p_run_id in integer,
	p_run_end in timestamp := null,
	p_run_result in varchar2 := null
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
end;

/


create or replace procedure dgrun_log
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


create or replace procedure dgparameter_insert
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
	p_par_keebdbruns in integer := null
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
		par_keebdbruns,
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
		p_par_keebdbruns,
		nvl(c_user, user),
		systimestamp
	);
	c_message := 'Parameter gespeichert';
end;

/


create or replace procedure dgparameter_update
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
	p_par_keebdbruns in integer := null
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
		par_keebdbruns = p_par_keebdbruns,
		par_uname = nvl(c_user, user),
		par_udate = systimestamp
	where
		par_id = p_par_id;
	c_message := 'Parameter gespeichert';
end;

/


create or replace procedure dgparameter_delete
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


create or replace procedure dgparameter_clone
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
	p_par_keebdbruns in integer := null
)
as
begin
	select seq_dgparameter.nextval into p_par_id from dual;

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
		par_keebdbruns,
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
		p_par_keebdbruns,
		nvl(c_user, user),
		systimestamp
	);
	c_message := 'Parameter gespeichert';
end;

/


create or replace procedure dgrun_start
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
	p_job_logfilename out varchar2,
	p_job_loglinkname out varchar2,
	p_job_pidfilename out varchar2,
	p_job_log2file out integer,
	p_job_log2db out integer,
	p_job_formatlogline out varchar2,
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
begin
	-- Create the project
	begin
		select pro_id into v_pro_id from dgproject where pro_name = p_pro_name;
	exception when no_data_found then
		dgproject_insert(c_user=>c_user, p_pro_id=>v_pro_id, p_pro_name=>p_pro_name);
	end;

	-- Create the job
	begin
		select
			job_id, job_logfilename, job_loglinkname, job_pidfilename, job_active
			into v_job_id, p_job_logfilename, p_job_loglinkname, p_job_pidfilename, p_job_active
		from
			dgjob
		where
			pro_id = v_pro_id and
			job_name = p_job_name;
	exception when no_data_found then
		dgjob_insert(
			c_user=>c_user,
			p_job_id=>v_job_id,
			p_pro_id=>v_pro_id,
			p_job_name=>p_job_name,
			p_job_active=>1
			 -- use global defaults for the rest of the arguments
		);
		p_job_active := 1;
	end;

	-- Get missing job parameters
	if p_job_logfilename is null then
		select par_logfilename into p_job_logfilename from dgparameter;
	end if;
	if p_job_loglinkname is null then
		select par_loglinkname into p_job_loglinkname from dgparameter;
	end if;
	if p_job_pidfilename is null then
		select par_pidfilename into p_job_pidfilename from dgparameter;
	end if;
	if p_job_log2file is null then
		select par_log2file into p_job_log2file from dgparameter;
	end if;
	if p_job_log2db is null then
		select par_log2db into p_job_log2db from dgparameter;
	end if;
	if p_job_formatlogline is null then
		select par_formatlogline into p_job_formatlogline from dgparameter;
	end if;
	select least(par_active, p_job_active) into p_job_active from dgparameter;

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

	-- Log the current script source
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

	-- Log the current crontab
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
		null, -- ok/failed not deternined yet
		null, -- no result
		v_scr_id,
		v_cron_id,
		nvl(c_user, user),
		systimestamp
	);
end;

/
