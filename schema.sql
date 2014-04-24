-- Table: boxes

-- DROP TABLE boxes;

CREATE TABLE boxes
(
  id uuid NOT NULL,
  name character varying(255),
  "desc" text,
  start_url character varying(255),
  icon_url character varying(255),
  website_url character varying(255),
  api_key uuid NOT NULL,
  master_key uuid NOT NULL,
  tenantname character varying(128) NOT NULL,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT boxes_pkey PRIMARY KEY (id),
  CONSTRAINT boxes_tenants_fkey FOREIGN KEY (tenantname)
      REFERENCES tenants (tenantname) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE boxes
  OWNER TO tardis;

-- Table: bots

-- DROP TABLE bots;

CREATE TABLE bots
(
  id serial NOT NULL,
  box_id uuid NOT NULL,
  name character varying(255),
  leverage character varying(255) CHECK (bot_functional(leverage)),
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT bots_pkey PRIMARY KEY (id),
  CONSTRAINT bots_boxes_fkey FOREIGN KEY (box_id)
      REFERENCES boxes (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE bots
  OWNER TO tardis;

-- Table: authorizations

-- DROP TABLE authorizations;

CREATE TABLE authorizations
(
  id serial NOT NULL,
  access_token character varying(255) UNIQUE NOT NULL,
  refresh_token character varying(255) UNIQUE NOT NULL,
  expires_at timestamp without time zone,
  scope text NOT NULL,
  origin character varying(255) NOT NULL,
  avatar_id integer NOT NULL,
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT authorizations_pkey PRIMARY KEY (id),
  CONSTRAINT authorizations_avatars_fkey FOREIGN KEY (avatar_id)
    REFERENCES avatars (id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE authorizations
  OWNER TO tardis;

-- Index: index_authorizations_on_access_token

-- DROP INDEX index_authorizations_on_access_token;

CREATE INDEX index_authorizations_on_access_token
  ON authorizations
  USING btree
  (access_token COLLATE pg_catalog."default");

-- Index: index_authorizations_on_refresh_token

-- DROP INDEX index_authorizations_on_refresh_token;

CREATE INDEX index_authorizations_on_refresh_token
  ON authorizations
  USING btree
  (refresh_token COLLATE pg_catalog."default");

-- Table: nodes

-- DROP TABLE nodes;

CREATE TABLE nodes
(
  id serial NOT NULL,
  box_id uuid NOT NULL,
  collection character varying(128) NOT NULL,
  data json,
  updated_at timestamp without time zone NOT NULL,
  avatar_id integer,
  CONSTRAINT nodes_pkey PRIMARY KEY (id),
  CONSTRAINT nodes_boxes_fkey FOREIGN KEY (box_id)
    REFERENCES boxes (id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT nodes_avatars_fkey FOREIGN KEY (avatar_id)
    REFERENCES avatars (id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE nodes
  OWNER TO tardis;

-- Index: index_nodes_on_collection

-- DROP INDEX index_nodes_on_collection;

CREATE INDEX index_nodes_on_collection
  ON nodes
  USING btree
  (collection COLLATE pg_catalog."default");

-- Table: roles

-- DROP TABLE roles;

CREATE TABLE roles
(
  role character varying(128) NOT NULL,
  level integer NOT NULL,
  CONSTRAINT roles_pkey PRIMARY KEY (role)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE roles
  OWNER TO tardis;
  
-- Table: tenants

-- DROP TABLE tenants;

CREATE TABLE tenants
(
  tenantname character varying(128) NOT NULL,
  role character varying(128),
  email character varying(128),
  "desc" character varying(128),
  crypted_password character varying(255),
  password_salt character varying(255),
  login_count integer,
  last_login_at timestamp without time zone,
  current_login_at timestamp without time zone,
  last_login_ip character varying(255),
  current_login_ip character varying(255),
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT tenants_pkey PRIMARY KEY (tenantname),
  CONSTRAINT tenants_role_fkey FOREIGN KEY (role)
      REFERENCES roles (role) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tenants
  OWNER TO tardis;

-- Index: index_tenants_on_email

-- DROP INDEX index_tenants_on_email;

CREATE INDEX index_tenants_on_email
  ON tenants
  USING btree
  (email COLLATE pg_catalog."default");

-- Table: avatars

-- DROP TABLE avatars;

CREATE TABLE avatars
(
  id serial NOT NULL,
  box_id uuid NOT NULL,
  login character varying(255),
  email character varying(128),
  "desc" character varying(128),
  crypted_password character varying(255),
  password_salt character varying(255),
  login_count integer,
  last_request_at timestamp without time zone,
  last_login_at timestamp without time zone,
  current_login_at timestamp without time zone,
  last_login_ip character varying(255),
  current_login_ip character varying(255),
  created_at timestamp without time zone,
  updated_at timestamp without time zone,
  CONSTRAINT avatars_boxes_fkey FOREIGN KEY (box_id)
    REFERENCES boxes (id) MATCH SIMPLE
    ON UPDATE NO ACTION ON DELETE NO ACTION,
  CONSTRAINT avatars_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE avatars
  OWNER TO tardis;

-- Index: index_avatars_on_box_id

-- DROP INDEX index_avatars_on_box_id;

CREATE INDEX index_avatars_on_box_id
  ON avatars
  USING btree
  (box_id COLLATE pg_catalog."default");

-- Index: index_avatars_on_email

-- DROP INDEX index_avatars_on_email;

CREATE INDEX index_avatars_on_email
  ON avatars
  USING btree
  (email COLLATE pg_catalog."default");

-- Index: index_avatars_on_last_request_at

-- DROP INDEX index_avatars_on_last_request_at;

CREATE INDEX index_avatars_on_last_request_at
  ON avatars
  USING btree
  (last_request_at);

-- Index: index_avatars_on_login

-- DROP INDEX index_avatars_on_login;

CREATE INDEX index_avatars_on_login
  ON avatars
  USING btree
  (login COLLATE pg_catalog."default");