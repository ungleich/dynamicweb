--
-- PostgreSQL database cluster dump
--

SET default_transaction_read_only = off;

SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;

--
-- Roles
--

CREATE ROLE app;
ALTER ROLE app WITH NOSUPERUSER INHERIT NOCREATEROLE CREATEDB LOGIN NOREPLICATION;
CREATE ROLE postgres;
ALTER ROLE postgres WITH SUPERUSER INHERIT CREATEROLE CREATEDB LOGIN REPLICATION;






--
-- Database creation
--

CREATE DATABASE app WITH TEMPLATE = template0 OWNER = app;
CREATE DATABASE appdb WITH TEMPLATE = template0 OWNER = app;
CREATE DATABASE dynamicweb WITH TEMPLATE = template0 OWNER = app;
REVOKE ALL ON DATABASE template1 FROM PUBLIC;
REVOKE ALL ON DATABASE template1 FROM postgres;
GRANT ALL ON DATABASE template1 TO postgres;
GRANT CONNECT ON DATABASE template1 TO PUBLIC;


\connect app

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE auth_group OWNER TO app;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_id_seq OWNER TO app;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_group_permissions OWNER TO app;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_permissions_id_seq OWNER TO app;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE auth_permission OWNER TO app;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_permission_id_seq OWNER TO app;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE auth_user OWNER TO app;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE auth_user_groups OWNER TO app;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_groups_id_seq OWNER TO app;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_id_seq OWNER TO app;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_user_user_permissions OWNER TO app;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_user_permissions_id_seq OWNER TO app;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: cms_aliaspluginmodel; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_aliaspluginmodel (
    cmsplugin_ptr_id integer NOT NULL,
    plugin_id integer,
    alias_placeholder_id integer
);


ALTER TABLE cms_aliaspluginmodel OWNER TO app;

--
-- Name: cms_cmsplugin; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_cmsplugin (
    id integer NOT NULL,
    "position" smallint,
    language character varying(15) NOT NULL,
    plugin_type character varying(50) NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    changed_date timestamp with time zone NOT NULL,
    parent_id integer,
    placeholder_id integer,
    depth integer NOT NULL,
    numchild integer NOT NULL,
    path character varying(255) NOT NULL,
    CONSTRAINT cms_cmsplugin_depth_check CHECK ((depth >= 0)),
    CONSTRAINT cms_cmsplugin_numchild_check CHECK ((numchild >= 0)),
    CONSTRAINT cms_cmsplugin_position_check CHECK (("position" >= 0))
);


ALTER TABLE cms_cmsplugin OWNER TO app;

--
-- Name: cms_cmsplugin_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_cmsplugin_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_cmsplugin_id_seq OWNER TO app;

--
-- Name: cms_cmsplugin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_cmsplugin_id_seq OWNED BY cms_cmsplugin.id;


--
-- Name: cms_globalpagepermission; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_globalpagepermission (
    id integer NOT NULL,
    can_change boolean NOT NULL,
    can_add boolean NOT NULL,
    can_delete boolean NOT NULL,
    can_change_advanced_settings boolean NOT NULL,
    can_publish boolean NOT NULL,
    can_change_permissions boolean NOT NULL,
    can_move_page boolean NOT NULL,
    can_view boolean NOT NULL,
    can_recover_page boolean NOT NULL,
    group_id integer,
    user_id integer
);


ALTER TABLE cms_globalpagepermission OWNER TO app;

--
-- Name: cms_globalpagepermission_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_globalpagepermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_globalpagepermission_id_seq OWNER TO app;

--
-- Name: cms_globalpagepermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_globalpagepermission_id_seq OWNED BY cms_globalpagepermission.id;


--
-- Name: cms_globalpagepermission_sites; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_globalpagepermission_sites (
    id integer NOT NULL,
    globalpagepermission_id integer NOT NULL,
    site_id integer NOT NULL
);


ALTER TABLE cms_globalpagepermission_sites OWNER TO app;

--
-- Name: cms_globalpagepermission_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_globalpagepermission_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_globalpagepermission_sites_id_seq OWNER TO app;

--
-- Name: cms_globalpagepermission_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_globalpagepermission_sites_id_seq OWNED BY cms_globalpagepermission_sites.id;


--
-- Name: cms_page; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_page (
    id integer NOT NULL,
    created_by character varying(255) NOT NULL,
    changed_by character varying(255) NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    changed_date timestamp with time zone NOT NULL,
    publication_date timestamp with time zone,
    publication_end_date timestamp with time zone,
    in_navigation boolean NOT NULL,
    soft_root boolean NOT NULL,
    reverse_id character varying(40),
    navigation_extenders character varying(80),
    template character varying(100) NOT NULL,
    login_required boolean NOT NULL,
    limit_visibility_in_menu smallint,
    is_home boolean NOT NULL,
    application_urls character varying(200),
    application_namespace character varying(200),
    publisher_is_draft boolean NOT NULL,
    languages character varying(255),
    revision_id integer NOT NULL,
    xframe_options integer NOT NULL,
    parent_id integer,
    publisher_public_id integer,
    site_id integer NOT NULL,
    depth integer NOT NULL,
    numchild integer NOT NULL,
    path character varying(255) NOT NULL,
    CONSTRAINT cms_page_depth_check CHECK ((depth >= 0)),
    CONSTRAINT cms_page_numchild_check CHECK ((numchild >= 0)),
    CONSTRAINT cms_page_revision_id_check CHECK ((revision_id >= 0))
);


ALTER TABLE cms_page OWNER TO app;

--
-- Name: cms_page_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_page_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_page_id_seq OWNER TO app;

--
-- Name: cms_page_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_page_id_seq OWNED BY cms_page.id;


--
-- Name: cms_page_placeholders; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_page_placeholders (
    id integer NOT NULL,
    page_id integer NOT NULL,
    placeholder_id integer NOT NULL
);


ALTER TABLE cms_page_placeholders OWNER TO app;

--
-- Name: cms_page_placeholders_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_page_placeholders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_page_placeholders_id_seq OWNER TO app;

--
-- Name: cms_page_placeholders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_page_placeholders_id_seq OWNED BY cms_page_placeholders.id;


--
-- Name: cms_pagepermission; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_pagepermission (
    id integer NOT NULL,
    can_change boolean NOT NULL,
    can_add boolean NOT NULL,
    can_delete boolean NOT NULL,
    can_change_advanced_settings boolean NOT NULL,
    can_publish boolean NOT NULL,
    can_change_permissions boolean NOT NULL,
    can_move_page boolean NOT NULL,
    can_view boolean NOT NULL,
    grant_on integer NOT NULL,
    group_id integer,
    page_id integer,
    user_id integer
);


ALTER TABLE cms_pagepermission OWNER TO app;

--
-- Name: cms_pagepermission_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_pagepermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_pagepermission_id_seq OWNER TO app;

--
-- Name: cms_pagepermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_pagepermission_id_seq OWNED BY cms_pagepermission.id;


--
-- Name: cms_pageuser; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_pageuser (
    user_ptr_id integer NOT NULL,
    created_by_id integer NOT NULL
);


ALTER TABLE cms_pageuser OWNER TO app;

--
-- Name: cms_pageusergroup; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_pageusergroup (
    group_ptr_id integer NOT NULL,
    created_by_id integer NOT NULL
);


ALTER TABLE cms_pageusergroup OWNER TO app;

--
-- Name: cms_placeholder; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_placeholder (
    id integer NOT NULL,
    slot character varying(255) NOT NULL,
    default_width smallint,
    CONSTRAINT cms_placeholder_default_width_check CHECK ((default_width >= 0))
);


ALTER TABLE cms_placeholder OWNER TO app;

--
-- Name: cms_placeholder_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_placeholder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_placeholder_id_seq OWNER TO app;

--
-- Name: cms_placeholder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_placeholder_id_seq OWNED BY cms_placeholder.id;


--
-- Name: cms_placeholderreference; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_placeholderreference (
    cmsplugin_ptr_id integer NOT NULL,
    name character varying(255) NOT NULL,
    placeholder_ref_id integer
);


ALTER TABLE cms_placeholderreference OWNER TO app;

--
-- Name: cms_staticplaceholder; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_staticplaceholder (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    code character varying(255) NOT NULL,
    dirty boolean NOT NULL,
    creation_method character varying(20) NOT NULL,
    draft_id integer,
    public_id integer,
    site_id integer
);


ALTER TABLE cms_staticplaceholder OWNER TO app;

--
-- Name: cms_staticplaceholder_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_staticplaceholder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_staticplaceholder_id_seq OWNER TO app;

--
-- Name: cms_staticplaceholder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_staticplaceholder_id_seq OWNED BY cms_staticplaceholder.id;


--
-- Name: cms_title; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_title (
    id integer NOT NULL,
    language character varying(15) NOT NULL,
    title character varying(255) NOT NULL,
    page_title character varying(255),
    menu_title character varying(255),
    meta_description text,
    slug character varying(255) NOT NULL,
    path character varying(255) NOT NULL,
    has_url_overwrite boolean NOT NULL,
    redirect character varying(2048),
    creation_date timestamp with time zone NOT NULL,
    published boolean NOT NULL,
    publisher_is_draft boolean NOT NULL,
    publisher_state smallint NOT NULL,
    page_id integer NOT NULL,
    publisher_public_id integer
);


ALTER TABLE cms_title OWNER TO app;

--
-- Name: cms_title_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_title_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_title_id_seq OWNER TO app;

--
-- Name: cms_title_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_title_id_seq OWNED BY cms_title.id;


--
-- Name: cms_usersettings; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_usersettings (
    id integer NOT NULL,
    language character varying(10) NOT NULL,
    clipboard_id integer,
    user_id integer NOT NULL
);


ALTER TABLE cms_usersettings OWNER TO app;

--
-- Name: cms_usersettings_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_usersettings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_usersettings_id_seq OWNER TO app;

--
-- Name: cms_usersettings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_usersettings_id_seq OWNED BY cms_usersettings.id;


--
-- Name: cmsplugin_filer_file_filerfile; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_file_filerfile (
    cmsplugin_ptr_id integer NOT NULL,
    title character varying(255),
    target_blank boolean NOT NULL,
    style character varying(255) NOT NULL,
    file_id integer NOT NULL
);


ALTER TABLE cmsplugin_filer_file_filerfile OWNER TO app;

--
-- Name: cmsplugin_filer_folder_filerfolder; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_folder_filerfolder (
    cmsplugin_ptr_id integer NOT NULL,
    title character varying(255),
    style character varying(50) NOT NULL,
    folder_id integer NOT NULL
);


ALTER TABLE cmsplugin_filer_folder_filerfolder OWNER TO app;

--
-- Name: cmsplugin_filer_image_filerimage; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_image_filerimage (
    cmsplugin_ptr_id integer NOT NULL,
    style character varying(50) NOT NULL,
    caption_text character varying(255),
    image_url character varying(200),
    alt_text character varying(255),
    use_original_image boolean NOT NULL,
    use_autoscale boolean NOT NULL,
    width integer,
    height integer,
    crop boolean NOT NULL,
    upscale boolean NOT NULL,
    alignment character varying(10),
    free_link character varying(255),
    original_link boolean NOT NULL,
    description text,
    target_blank boolean NOT NULL,
    file_link_id integer,
    image_id integer,
    page_link_id integer,
    thumbnail_option_id integer,
    CONSTRAINT cmsplugin_filer_image_filerimage_height_check CHECK ((height >= 0)),
    CONSTRAINT cmsplugin_filer_image_filerimage_width_check CHECK ((width >= 0))
);


ALTER TABLE cmsplugin_filer_image_filerimage OWNER TO app;

--
-- Name: cmsplugin_filer_image_thumbnailoption; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_image_thumbnailoption (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    width integer NOT NULL,
    height integer NOT NULL,
    crop boolean NOT NULL,
    upscale boolean NOT NULL
);


ALTER TABLE cmsplugin_filer_image_thumbnailoption OWNER TO app;

--
-- Name: cmsplugin_filer_image_thumbnailoption_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cmsplugin_filer_image_thumbnailoption_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cmsplugin_filer_image_thumbnailoption_id_seq OWNER TO app;

--
-- Name: cmsplugin_filer_image_thumbnailoption_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cmsplugin_filer_image_thumbnailoption_id_seq OWNED BY cmsplugin_filer_image_thumbnailoption.id;


--
-- Name: cmsplugin_filer_link_filerlinkplugin; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_link_filerlinkplugin (
    cmsplugin_ptr_id integer NOT NULL,
    name character varying(255) NOT NULL,
    url character varying(255),
    mailto character varying(75),
    link_style character varying(255) NOT NULL,
    new_window boolean NOT NULL,
    file_id integer,
    page_link_id integer
);


ALTER TABLE cmsplugin_filer_link_filerlinkplugin OWNER TO app;

--
-- Name: cmsplugin_filer_teaser_filerteaser; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_teaser_filerteaser (
    cmsplugin_ptr_id integer NOT NULL,
    title character varying(255) NOT NULL,
    image_url character varying(200),
    style character varying(255) NOT NULL,
    use_autoscale boolean NOT NULL,
    width integer,
    height integer,
    free_link character varying(255),
    description text,
    target_blank boolean NOT NULL,
    image_id integer,
    page_link_id integer,
    CONSTRAINT cmsplugin_filer_teaser_filerteaser_height_check CHECK ((height >= 0)),
    CONSTRAINT cmsplugin_filer_teaser_filerteaser_width_check CHECK ((width >= 0))
);


ALTER TABLE cmsplugin_filer_teaser_filerteaser OWNER TO app;

--
-- Name: cmsplugin_filer_video_filervideo; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_video_filervideo (
    cmsplugin_ptr_id integer NOT NULL,
    movie_url character varying(255),
    width smallint NOT NULL,
    height smallint NOT NULL,
    auto_play boolean NOT NULL,
    auto_hide boolean NOT NULL,
    fullscreen boolean NOT NULL,
    loop boolean NOT NULL,
    bgcolor character varying(6) NOT NULL,
    textcolor character varying(6) NOT NULL,
    seekbarcolor character varying(6) NOT NULL,
    seekbarbgcolor character varying(6) NOT NULL,
    loadingbarcolor character varying(6) NOT NULL,
    buttonoutcolor character varying(6) NOT NULL,
    buttonovercolor character varying(6) NOT NULL,
    buttonhighlightcolor character varying(6) NOT NULL,
    image_id integer,
    movie_id integer,
    CONSTRAINT cmsplugin_filer_video_filervideo_height_check CHECK ((height >= 0)),
    CONSTRAINT cmsplugin_filer_video_filervideo_width_check CHECK ((width >= 0))
);


ALTER TABLE cmsplugin_filer_video_filervideo OWNER TO app;

--
-- Name: digitalglarus_dggallery; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE digitalglarus_dggallery (
    id integer NOT NULL,
    name character varying(30) NOT NULL,
    parent_id integer
);


ALTER TABLE digitalglarus_dggallery OWNER TO app;

--
-- Name: digitalglarus_dggallery_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE digitalglarus_dggallery_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE digitalglarus_dggallery_id_seq OWNER TO app;

--
-- Name: digitalglarus_dggallery_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE digitalglarus_dggallery_id_seq OWNED BY digitalglarus_dggallery.id;


--
-- Name: digitalglarus_dggalleryplugin; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE digitalglarus_dggalleryplugin (
    cmsplugin_ptr_id integer NOT NULL,
    "dgGallery_id" integer NOT NULL
);


ALTER TABLE digitalglarus_dggalleryplugin OWNER TO app;

--
-- Name: digitalglarus_dgpicture; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE digitalglarus_dgpicture (
    id integer NOT NULL,
    description character varying(60) NOT NULL,
    gallery_id integer NOT NULL,
    image_id integer NOT NULL
);


ALTER TABLE digitalglarus_dgpicture OWNER TO app;

--
-- Name: digitalglarus_dgpicture_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE digitalglarus_dgpicture_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE digitalglarus_dgpicture_id_seq OWNER TO app;

--
-- Name: digitalglarus_dgpicture_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE digitalglarus_dgpicture_id_seq OWNED BY digitalglarus_dgpicture.id;


--
-- Name: digitalglarus_dgsupportersplugin; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE digitalglarus_dgsupportersplugin (
    cmsplugin_ptr_id integer NOT NULL
);


ALTER TABLE digitalglarus_dgsupportersplugin OWNER TO app;

--
-- Name: digitalglarus_message; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE digitalglarus_message (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    email character varying(75) NOT NULL,
    phone_number character varying(200) NOT NULL,
    message text NOT NULL,
    received_date timestamp with time zone NOT NULL
);


ALTER TABLE digitalglarus_message OWNER TO app;

--
-- Name: digitalglarus_message_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE digitalglarus_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE digitalglarus_message_id_seq OWNER TO app;

--
-- Name: digitalglarus_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE digitalglarus_message_id_seq OWNED BY digitalglarus_message.id;


--
-- Name: digitalglarus_supporter; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE digitalglarus_supporter (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    description text
);


ALTER TABLE digitalglarus_supporter OWNER TO app;

--
-- Name: digitalglarus_supporter_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE digitalglarus_supporter_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE digitalglarus_supporter_id_seq OWNER TO app;

--
-- Name: digitalglarus_supporter_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE digitalglarus_supporter_id_seq OWNED BY digitalglarus_supporter.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE django_admin_log OWNER TO app;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_admin_log_id_seq OWNER TO app;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO app;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_content_type_id_seq OWNER TO app;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO app;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO app;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_select2_keymap; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE django_select2_keymap (
    id integer NOT NULL,
    key character varying(40) NOT NULL,
    value character varying(100) NOT NULL,
    accessed_on timestamp with time zone NOT NULL
);


ALTER TABLE django_select2_keymap OWNER TO app;

--
-- Name: django_select2_keymap_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE django_select2_keymap_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_select2_keymap_id_seq OWNER TO app;

--
-- Name: django_select2_keymap_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE django_select2_keymap_id_seq OWNED BY django_select2_keymap.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE django_session OWNER TO app;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE django_site OWNER TO app;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_site_id_seq OWNER TO app;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: djangocms_blog_authorentriesplugin; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_authorentriesplugin (
    cmsplugin_ptr_id integer NOT NULL,
    latest_posts integer NOT NULL
);


ALTER TABLE djangocms_blog_authorentriesplugin OWNER TO app;

--
-- Name: djangocms_blog_authorentriesplugin_authors; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_authorentriesplugin_authors (
    id integer NOT NULL,
    authorentriesplugin_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE djangocms_blog_authorentriesplugin_authors OWNER TO app;

--
-- Name: djangocms_blog_authorentriesplugin_authors_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_authorentriesplugin_authors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_authorentriesplugin_authors_id_seq OWNER TO app;

--
-- Name: djangocms_blog_authorentriesplugin_authors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_authorentriesplugin_authors_id_seq OWNED BY djangocms_blog_authorentriesplugin_authors.id;


--
-- Name: djangocms_blog_blogcategory; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_blogcategory (
    id integer NOT NULL,
    date_created timestamp with time zone NOT NULL,
    date_modified timestamp with time zone NOT NULL,
    parent_id integer
);


ALTER TABLE djangocms_blog_blogcategory OWNER TO app;

--
-- Name: djangocms_blog_blogcategory_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_blogcategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_blogcategory_id_seq OWNER TO app;

--
-- Name: djangocms_blog_blogcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_blogcategory_id_seq OWNED BY djangocms_blog_blogcategory.id;


--
-- Name: djangocms_blog_blogcategory_translation; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_blogcategory_translation (
    id integer NOT NULL,
    language_code character varying(15) NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(50) NOT NULL,
    master_id integer
);


ALTER TABLE djangocms_blog_blogcategory_translation OWNER TO app;

--
-- Name: djangocms_blog_blogcategory_translation_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_blogcategory_translation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_blogcategory_translation_id_seq OWNER TO app;

--
-- Name: djangocms_blog_blogcategory_translation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_blogcategory_translation_id_seq OWNED BY djangocms_blog_blogcategory_translation.id;


--
-- Name: djangocms_blog_latestpostsplugin; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_latestpostsplugin (
    cmsplugin_ptr_id integer NOT NULL,
    latest_posts integer NOT NULL
);


ALTER TABLE djangocms_blog_latestpostsplugin OWNER TO app;

--
-- Name: djangocms_blog_latestpostsplugin_categories; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_latestpostsplugin_categories (
    id integer NOT NULL,
    latestpostsplugin_id integer NOT NULL,
    blogcategory_id integer NOT NULL
);


ALTER TABLE djangocms_blog_latestpostsplugin_categories OWNER TO app;

--
-- Name: djangocms_blog_latestpostsplugin_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_latestpostsplugin_categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_latestpostsplugin_categories_id_seq OWNER TO app;

--
-- Name: djangocms_blog_latestpostsplugin_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_latestpostsplugin_categories_id_seq OWNED BY djangocms_blog_latestpostsplugin_categories.id;


--
-- Name: djangocms_blog_latestpostsplugin_tags; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_latestpostsplugin_tags (
    id integer NOT NULL,
    latestpostsplugin_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE djangocms_blog_latestpostsplugin_tags OWNER TO app;

--
-- Name: djangocms_blog_latestpostsplugin_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_latestpostsplugin_tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_latestpostsplugin_tags_id_seq OWNER TO app;

--
-- Name: djangocms_blog_latestpostsplugin_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_latestpostsplugin_tags_id_seq OWNED BY djangocms_blog_latestpostsplugin_tags.id;


--
-- Name: djangocms_blog_post; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_post (
    id integer NOT NULL,
    date_created timestamp with time zone NOT NULL,
    date_modified timestamp with time zone NOT NULL,
    date_published timestamp with time zone NOT NULL,
    date_published_end timestamp with time zone,
    publish boolean NOT NULL,
    enable_comments boolean NOT NULL,
    author_id integer,
    content_id integer,
    main_image_id integer,
    main_image_full_id integer,
    main_image_thumbnail_id integer
);


ALTER TABLE djangocms_blog_post OWNER TO app;

--
-- Name: djangocms_blog_post_categories; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_post_categories (
    id integer NOT NULL,
    post_id integer NOT NULL,
    blogcategory_id integer NOT NULL
);


ALTER TABLE djangocms_blog_post_categories OWNER TO app;

--
-- Name: djangocms_blog_post_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_post_categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_post_categories_id_seq OWNER TO app;

--
-- Name: djangocms_blog_post_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_post_categories_id_seq OWNED BY djangocms_blog_post_categories.id;


--
-- Name: djangocms_blog_post_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_post_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_post_id_seq OWNER TO app;

--
-- Name: djangocms_blog_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_post_id_seq OWNED BY djangocms_blog_post.id;


--
-- Name: djangocms_blog_post_sites; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_post_sites (
    id integer NOT NULL,
    post_id integer NOT NULL,
    site_id integer NOT NULL
);


ALTER TABLE djangocms_blog_post_sites OWNER TO app;

--
-- Name: djangocms_blog_post_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_post_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_post_sites_id_seq OWNER TO app;

--
-- Name: djangocms_blog_post_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_post_sites_id_seq OWNED BY djangocms_blog_post_sites.id;


--
-- Name: djangocms_blog_post_translation; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_post_translation (
    id integer NOT NULL,
    language_code character varying(15) NOT NULL,
    title character varying(255) NOT NULL,
    slug character varying(50) NOT NULL,
    abstract text NOT NULL,
    meta_description text NOT NULL,
    meta_keywords text NOT NULL,
    meta_title character varying(255) NOT NULL,
    post_text text NOT NULL,
    master_id integer
);


ALTER TABLE djangocms_blog_post_translation OWNER TO app;

--
-- Name: djangocms_blog_post_translation_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_post_translation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_post_translation_id_seq OWNER TO app;

--
-- Name: djangocms_blog_post_translation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_post_translation_id_seq OWNED BY djangocms_blog_post_translation.id;


--
-- Name: djangocms_flash_flash; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_flash_flash (
    cmsplugin_ptr_id integer NOT NULL,
    file character varying(100) NOT NULL,
    width character varying(6) NOT NULL,
    height character varying(6) NOT NULL
);


ALTER TABLE djangocms_flash_flash OWNER TO app;

--
-- Name: djangocms_googlemap_googlemap; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_googlemap_googlemap (
    cmsplugin_ptr_id integer NOT NULL,
    title character varying(100),
    address character varying(150) NOT NULL,
    zipcode character varying(30) NOT NULL,
    city character varying(100) NOT NULL,
    content character varying(255) NOT NULL,
    zoom smallint NOT NULL,
    lat numeric(10,6),
    lng numeric(10,6),
    route_planer_title character varying(150),
    route_planer boolean NOT NULL,
    width character varying(6) NOT NULL,
    height character varying(6) NOT NULL,
    info_window boolean NOT NULL,
    scrollwheel boolean NOT NULL,
    double_click_zoom boolean NOT NULL,
    draggable boolean NOT NULL,
    keyboard_shortcuts boolean NOT NULL,
    pan_control boolean NOT NULL,
    zoom_control boolean NOT NULL,
    street_view_control boolean NOT NULL,
    CONSTRAINT djangocms_googlemap_googlemap_zoom_check CHECK ((zoom >= 0))
);


ALTER TABLE djangocms_googlemap_googlemap OWNER TO app;

--
-- Name: djangocms_inherit_inheritpageplaceholder; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_inherit_inheritpageplaceholder (
    cmsplugin_ptr_id integer NOT NULL,
    from_language character varying(5),
    from_page_id integer
);


ALTER TABLE djangocms_inherit_inheritpageplaceholder OWNER TO app;

--
-- Name: djangocms_link_link; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_link_link (
    cmsplugin_ptr_id integer NOT NULL,
    name character varying(256) NOT NULL,
    url character varying(2048),
    anchor character varying(128) NOT NULL,
    mailto character varying(75),
    phone character varying(40),
    target character varying(100) NOT NULL,
    page_link_id integer
);


ALTER TABLE djangocms_link_link OWNER TO app;

--
-- Name: djangocms_page_meta_pagemeta; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_page_meta_pagemeta (
    id integer NOT NULL,
    og_type character varying(255) NOT NULL,
    og_author_url character varying(255) NOT NULL,
    og_author_fbid character varying(16) NOT NULL,
    og_publisher character varying(255) NOT NULL,
    og_app_id character varying(255) NOT NULL,
    twitter_author character varying(255) NOT NULL,
    twitter_site character varying(255) NOT NULL,
    twitter_type character varying(255) NOT NULL,
    gplus_author character varying(255) NOT NULL,
    gplus_type character varying(255) NOT NULL,
    extended_object_id integer NOT NULL,
    image_id integer,
    og_author_id integer,
    public_extension_id integer
);


ALTER TABLE djangocms_page_meta_pagemeta OWNER TO app;

--
-- Name: djangocms_page_meta_pagemeta_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_page_meta_pagemeta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_page_meta_pagemeta_id_seq OWNER TO app;

--
-- Name: djangocms_page_meta_pagemeta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_page_meta_pagemeta_id_seq OWNED BY djangocms_page_meta_pagemeta.id;


--
-- Name: djangocms_page_meta_titlemeta; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_page_meta_titlemeta (
    id integer NOT NULL,
    keywords character varying(400) NOT NULL,
    description character varying(400) NOT NULL,
    og_description character varying(400) NOT NULL,
    twitter_description character varying(140) NOT NULL,
    gplus_description character varying(400) NOT NULL,
    extended_object_id integer NOT NULL,
    image_id integer,
    public_extension_id integer
);


ALTER TABLE djangocms_page_meta_titlemeta OWNER TO app;

--
-- Name: djangocms_page_meta_titlemeta_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_page_meta_titlemeta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_page_meta_titlemeta_id_seq OWNER TO app;

--
-- Name: djangocms_page_meta_titlemeta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_page_meta_titlemeta_id_seq OWNED BY djangocms_page_meta_titlemeta.id;


--
-- Name: djangocms_snippet_snippet; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_snippet_snippet (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    html text NOT NULL,
    template character varying(50) NOT NULL
);


ALTER TABLE djangocms_snippet_snippet OWNER TO app;

--
-- Name: djangocms_snippet_snippet_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_snippet_snippet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_snippet_snippet_id_seq OWNER TO app;

--
-- Name: djangocms_snippet_snippet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_snippet_snippet_id_seq OWNED BY djangocms_snippet_snippet.id;


--
-- Name: djangocms_snippet_snippetptr; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_snippet_snippetptr (
    cmsplugin_ptr_id integer NOT NULL,
    snippet_id integer NOT NULL
);


ALTER TABLE djangocms_snippet_snippetptr OWNER TO app;

--
-- Name: djangocms_teaser_teaser; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_teaser_teaser (
    cmsplugin_ptr_id integer NOT NULL,
    title character varying(255) NOT NULL,
    image character varying(100),
    url character varying(255),
    description text,
    page_link_id integer
);


ALTER TABLE djangocms_teaser_teaser OWNER TO app;

--
-- Name: djangocms_text_ckeditor_text; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_text_ckeditor_text (
    cmsplugin_ptr_id integer NOT NULL,
    body text NOT NULL
);


ALTER TABLE djangocms_text_ckeditor_text OWNER TO app;

--
-- Name: easy_thumbnails_source; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE easy_thumbnails_source (
    id integer NOT NULL,
    storage_hash character varying(40) NOT NULL,
    name character varying(255) NOT NULL,
    modified timestamp with time zone NOT NULL
);


ALTER TABLE easy_thumbnails_source OWNER TO app;

--
-- Name: easy_thumbnails_source_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE easy_thumbnails_source_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE easy_thumbnails_source_id_seq OWNER TO app;

--
-- Name: easy_thumbnails_source_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE easy_thumbnails_source_id_seq OWNED BY easy_thumbnails_source.id;


--
-- Name: easy_thumbnails_thumbnail; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE easy_thumbnails_thumbnail (
    id integer NOT NULL,
    storage_hash character varying(40) NOT NULL,
    name character varying(255) NOT NULL,
    modified timestamp with time zone NOT NULL,
    source_id integer NOT NULL
);


ALTER TABLE easy_thumbnails_thumbnail OWNER TO app;

--
-- Name: easy_thumbnails_thumbnail_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE easy_thumbnails_thumbnail_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE easy_thumbnails_thumbnail_id_seq OWNER TO app;

--
-- Name: easy_thumbnails_thumbnail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE easy_thumbnails_thumbnail_id_seq OWNED BY easy_thumbnails_thumbnail.id;


--
-- Name: easy_thumbnails_thumbnaildimensions; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE easy_thumbnails_thumbnaildimensions (
    id integer NOT NULL,
    thumbnail_id integer NOT NULL,
    width integer,
    height integer,
    CONSTRAINT easy_thumbnails_thumbnaildimensions_height_check CHECK ((height >= 0)),
    CONSTRAINT easy_thumbnails_thumbnaildimensions_width_check CHECK ((width >= 0))
);


ALTER TABLE easy_thumbnails_thumbnaildimensions OWNER TO app;

--
-- Name: easy_thumbnails_thumbnaildimensions_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE easy_thumbnails_thumbnaildimensions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE easy_thumbnails_thumbnaildimensions_id_seq OWNER TO app;

--
-- Name: easy_thumbnails_thumbnaildimensions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE easy_thumbnails_thumbnaildimensions_id_seq OWNED BY easy_thumbnails_thumbnaildimensions.id;


--
-- Name: filer_clipboard; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE filer_clipboard (
    id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE filer_clipboard OWNER TO app;

--
-- Name: filer_clipboard_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE filer_clipboard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE filer_clipboard_id_seq OWNER TO app;

--
-- Name: filer_clipboard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE filer_clipboard_id_seq OWNED BY filer_clipboard.id;


--
-- Name: filer_clipboarditem; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE filer_clipboarditem (
    id integer NOT NULL,
    clipboard_id integer NOT NULL,
    file_id integer NOT NULL
);


ALTER TABLE filer_clipboarditem OWNER TO app;

--
-- Name: filer_clipboarditem_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE filer_clipboarditem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE filer_clipboarditem_id_seq OWNER TO app;

--
-- Name: filer_clipboarditem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE filer_clipboarditem_id_seq OWNED BY filer_clipboarditem.id;


--
-- Name: filer_file; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE filer_file (
    id integer NOT NULL,
    file character varying(255),
    _file_size integer,
    sha1 character varying(40) NOT NULL,
    has_all_mandatory_data boolean NOT NULL,
    original_filename character varying(255),
    name character varying(255) NOT NULL,
    description text,
    uploaded_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    is_public boolean NOT NULL,
    folder_id integer,
    owner_id integer,
    polymorphic_ctype_id integer
);


ALTER TABLE filer_file OWNER TO app;

--
-- Name: filer_file_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE filer_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE filer_file_id_seq OWNER TO app;

--
-- Name: filer_file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE filer_file_id_seq OWNED BY filer_file.id;


--
-- Name: filer_folder; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE filer_folder (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    uploaded_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    lft integer NOT NULL,
    rght integer NOT NULL,
    tree_id integer NOT NULL,
    level integer NOT NULL,
    owner_id integer,
    parent_id integer,
    CONSTRAINT filer_folder_level_check CHECK ((level >= 0)),
    CONSTRAINT filer_folder_lft_check CHECK ((lft >= 0)),
    CONSTRAINT filer_folder_rght_check CHECK ((rght >= 0)),
    CONSTRAINT filer_folder_tree_id_check CHECK ((tree_id >= 0))
);


ALTER TABLE filer_folder OWNER TO app;

--
-- Name: filer_folder_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE filer_folder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE filer_folder_id_seq OWNER TO app;

--
-- Name: filer_folder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE filer_folder_id_seq OWNED BY filer_folder.id;


--
-- Name: filer_folderpermission; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE filer_folderpermission (
    id integer NOT NULL,
    type smallint NOT NULL,
    everybody boolean NOT NULL,
    can_edit smallint,
    can_read smallint,
    can_add_children smallint,
    folder_id integer,
    group_id integer,
    user_id integer
);


ALTER TABLE filer_folderpermission OWNER TO app;

--
-- Name: filer_folderpermission_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE filer_folderpermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE filer_folderpermission_id_seq OWNER TO app;

--
-- Name: filer_folderpermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE filer_folderpermission_id_seq OWNED BY filer_folderpermission.id;


--
-- Name: filer_image; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE filer_image (
    file_ptr_id integer NOT NULL,
    _height integer,
    _width integer,
    date_taken timestamp with time zone,
    default_alt_text character varying(255),
    default_caption character varying(255),
    author character varying(255),
    must_always_publish_author_credit boolean NOT NULL,
    must_always_publish_copyright boolean NOT NULL,
    subject_location character varying(64)
);


ALTER TABLE filer_image OWNER TO app;

--
-- Name: hosting_railsbetauser; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE hosting_railsbetauser (
    id integer NOT NULL,
    email character varying(75) NOT NULL,
    received_date timestamp with time zone NOT NULL
);


ALTER TABLE hosting_railsbetauser OWNER TO app;

--
-- Name: hosting_railsbetauser_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE hosting_railsbetauser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE hosting_railsbetauser_id_seq OWNER TO app;

--
-- Name: hosting_railsbetauser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE hosting_railsbetauser_id_seq OWNED BY hosting_railsbetauser.id;


--
-- Name: menus_cachekey; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE menus_cachekey (
    id integer NOT NULL,
    language character varying(255) NOT NULL,
    site integer NOT NULL,
    key character varying(255) NOT NULL,
    CONSTRAINT menus_cachekey_site_check CHECK ((site >= 0))
);


ALTER TABLE menus_cachekey OWNER TO app;

--
-- Name: menus_cachekey_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE menus_cachekey_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE menus_cachekey_id_seq OWNER TO app;

--
-- Name: menus_cachekey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE menus_cachekey_id_seq OWNED BY menus_cachekey.id;


--
-- Name: railshosting_railsbetauser; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE railshosting_railsbetauser (
    id integer NOT NULL,
    email character varying(75) NOT NULL,
    received_date timestamp with time zone NOT NULL
);


ALTER TABLE railshosting_railsbetauser OWNER TO app;

--
-- Name: railshosting_railsbetauser_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE railshosting_railsbetauser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE railshosting_railsbetauser_id_seq OWNER TO app;

--
-- Name: railshosting_railsbetauser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE railshosting_railsbetauser_id_seq OWNED BY railshosting_railsbetauser.id;


--
-- Name: reversion_revision; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE reversion_revision (
    id integer NOT NULL,
    manager_slug character varying(191) NOT NULL,
    date_created timestamp with time zone NOT NULL,
    comment text NOT NULL,
    user_id integer
);


ALTER TABLE reversion_revision OWNER TO app;

--
-- Name: reversion_revision_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE reversion_revision_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE reversion_revision_id_seq OWNER TO app;

--
-- Name: reversion_revision_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE reversion_revision_id_seq OWNED BY reversion_revision.id;


--
-- Name: reversion_version; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE reversion_version (
    id integer NOT NULL,
    object_id text NOT NULL,
    object_id_int integer,
    format character varying(255) NOT NULL,
    serialized_data text NOT NULL,
    object_repr text NOT NULL,
    content_type_id integer NOT NULL,
    revision_id integer NOT NULL
);


ALTER TABLE reversion_version OWNER TO app;

--
-- Name: reversion_version_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE reversion_version_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE reversion_version_id_seq OWNER TO app;

--
-- Name: reversion_version_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE reversion_version_id_seq OWNED BY reversion_version.id;


--
-- Name: taggit_tag; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE taggit_tag (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL
);


ALTER TABLE taggit_tag OWNER TO app;

--
-- Name: taggit_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE taggit_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE taggit_tag_id_seq OWNER TO app;

--
-- Name: taggit_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE taggit_tag_id_seq OWNED BY taggit_tag.id;


--
-- Name: taggit_taggeditem; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE taggit_taggeditem (
    id integer NOT NULL,
    object_id integer NOT NULL,
    content_type_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE taggit_taggeditem OWNER TO app;

--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE taggit_taggeditem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE taggit_taggeditem_id_seq OWNER TO app;

--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE taggit_taggeditem_id_seq OWNED BY taggit_taggeditem.id;


--
-- Name: ungleich_ungleichpage; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE ungleich_ungleichpage (
    id integer NOT NULL,
    extended_object_id integer NOT NULL,
    public_extension_id integer,
    image_id integer
);


ALTER TABLE ungleich_ungleichpage OWNER TO app;

--
-- Name: ungleich_ungleichpage_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE ungleich_ungleichpage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ungleich_ungleichpage_id_seq OWNER TO app;

--
-- Name: ungleich_ungleichpage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE ungleich_ungleichpage_id_seq OWNED BY ungleich_ungleichpage.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_cmsplugin ALTER COLUMN id SET DEFAULT nextval('cms_cmsplugin_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_globalpagepermission ALTER COLUMN id SET DEFAULT nextval('cms_globalpagepermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_globalpagepermission_sites ALTER COLUMN id SET DEFAULT nextval('cms_globalpagepermission_sites_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page ALTER COLUMN id SET DEFAULT nextval('cms_page_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page_placeholders ALTER COLUMN id SET DEFAULT nextval('cms_page_placeholders_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pagepermission ALTER COLUMN id SET DEFAULT nextval('cms_pagepermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_placeholder ALTER COLUMN id SET DEFAULT nextval('cms_placeholder_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_staticplaceholder ALTER COLUMN id SET DEFAULT nextval('cms_staticplaceholder_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_title ALTER COLUMN id SET DEFAULT nextval('cms_title_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_usersettings ALTER COLUMN id SET DEFAULT nextval('cms_usersettings_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_image_thumbnailoption ALTER COLUMN id SET DEFAULT nextval('cmsplugin_filer_image_thumbnailoption_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY digitalglarus_dggallery ALTER COLUMN id SET DEFAULT nextval('digitalglarus_dggallery_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY digitalglarus_dgpicture ALTER COLUMN id SET DEFAULT nextval('digitalglarus_dgpicture_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY digitalglarus_message ALTER COLUMN id SET DEFAULT nextval('digitalglarus_message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY digitalglarus_supporter ALTER COLUMN id SET DEFAULT nextval('digitalglarus_supporter_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_select2_keymap ALTER COLUMN id SET DEFAULT nextval('django_select2_keymap_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin_authors ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_authorentriesplugin_authors_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_blogcategory ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_blogcategory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_blogcategory_translation ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_blogcategory_translation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_categories ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_latestpostsplugin_categories_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_tags ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_latestpostsplugin_tags_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_post_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_categories ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_post_categories_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_sites ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_post_sites_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_translation ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_post_translation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_page_meta_pagemeta ALTER COLUMN id SET DEFAULT nextval('djangocms_page_meta_pagemeta_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_page_meta_titlemeta ALTER COLUMN id SET DEFAULT nextval('djangocms_page_meta_titlemeta_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_snippet_snippet ALTER COLUMN id SET DEFAULT nextval('djangocms_snippet_snippet_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY easy_thumbnails_source ALTER COLUMN id SET DEFAULT nextval('easy_thumbnails_source_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY easy_thumbnails_thumbnail ALTER COLUMN id SET DEFAULT nextval('easy_thumbnails_thumbnail_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY easy_thumbnails_thumbnaildimensions ALTER COLUMN id SET DEFAULT nextval('easy_thumbnails_thumbnaildimensions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_clipboard ALTER COLUMN id SET DEFAULT nextval('filer_clipboard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_clipboarditem ALTER COLUMN id SET DEFAULT nextval('filer_clipboarditem_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_file ALTER COLUMN id SET DEFAULT nextval('filer_file_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folder ALTER COLUMN id SET DEFAULT nextval('filer_folder_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folderpermission ALTER COLUMN id SET DEFAULT nextval('filer_folderpermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY hosting_railsbetauser ALTER COLUMN id SET DEFAULT nextval('hosting_railsbetauser_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY menus_cachekey ALTER COLUMN id SET DEFAULT nextval('menus_cachekey_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY railshosting_railsbetauser ALTER COLUMN id SET DEFAULT nextval('railshosting_railsbetauser_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY reversion_revision ALTER COLUMN id SET DEFAULT nextval('reversion_revision_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY reversion_version ALTER COLUMN id SET DEFAULT nextval('reversion_version_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY taggit_tag ALTER COLUMN id SET DEFAULT nextval('taggit_tag_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY taggit_taggeditem ALTER COLUMN id SET DEFAULT nextval('taggit_taggeditem_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY ungleich_ungleichpage ALTER COLUMN id SET DEFAULT nextval('ungleich_ungleichpage_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: app
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: app
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: app
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add site	7	add_site
20	Can change site	7	change_site
21	Can delete site	7	delete_site
22	Can add user setting	8	add_usersettings
23	Can change user setting	8	change_usersettings
24	Can delete user setting	8	delete_usersettings
25	Can add placeholder	9	add_placeholder
26	Can change placeholder	9	change_placeholder
27	Can delete placeholder	9	delete_placeholder
28	Can use Structure mode	9	use_structure
29	Can add cms plugin	10	add_cmsplugin
30	Can change cms plugin	10	change_cmsplugin
31	Can delete cms plugin	10	delete_cmsplugin
32	Can add page	11	add_page
33	Can change page	11	change_page
34	Can delete page	11	delete_page
35	Can view page	11	view_page
36	Can publish page	11	publish_page
37	Can edit static placeholders	11	edit_static_placeholder
38	Can add Page global permission	12	add_globalpagepermission
39	Can change Page global permission	12	change_globalpagepermission
40	Can delete Page global permission	12	delete_globalpagepermission
41	Can add Page permission	13	add_pagepermission
42	Can change Page permission	13	change_pagepermission
43	Can delete Page permission	13	delete_pagepermission
44	Can add User (page)	14	add_pageuser
45	Can change User (page)	14	change_pageuser
46	Can delete User (page)	14	delete_pageuser
47	Can add User group (page)	15	add_pageusergroup
48	Can change User group (page)	15	change_pageusergroup
49	Can delete User group (page)	15	delete_pageusergroup
50	Can add title	16	add_title
51	Can change title	16	change_title
52	Can delete title	16	delete_title
53	Can add placeholder reference	17	add_placeholderreference
54	Can change placeholder reference	17	change_placeholderreference
55	Can delete placeholder reference	17	delete_placeholderreference
56	Can add static placeholder	18	add_staticplaceholder
57	Can change static placeholder	18	change_staticplaceholder
58	Can delete static placeholder	18	delete_staticplaceholder
59	Can add alias plugin model	19	add_aliaspluginmodel
60	Can change alias plugin model	19	change_aliaspluginmodel
61	Can delete alias plugin model	19	delete_aliaspluginmodel
62	Can add cache key	20	add_cachekey
63	Can change cache key	20	change_cachekey
64	Can delete cache key	20	delete_cachekey
65	Can add flash	21	add_flash
66	Can change flash	21	change_flash
67	Can delete flash	21	delete_flash
68	Can add google map	22	add_googlemap
69	Can change google map	22	change_googlemap
70	Can delete google map	22	delete_googlemap
71	Can add inherit page placeholder	23	add_inheritpageplaceholder
72	Can change inherit page placeholder	23	change_inheritpageplaceholder
73	Can delete inherit page placeholder	23	delete_inheritpageplaceholder
74	Can add link	24	add_link
75	Can change link	24	change_link
76	Can delete link	24	delete_link
77	Can add Snippet	25	add_snippet
78	Can change Snippet	25	change_snippet
79	Can delete Snippet	25	delete_snippet
80	Can add Snippet	26	add_snippetptr
81	Can change Snippet	26	change_snippetptr
82	Can delete Snippet	26	delete_snippetptr
83	Can add teaser	27	add_teaser
84	Can change teaser	27	change_teaser
85	Can delete teaser	27	delete_teaser
86	Can add filer file	28	add_filerfile
87	Can change filer file	28	change_filerfile
88	Can delete filer file	28	delete_filerfile
89	Can add filer folder	29	add_filerfolder
90	Can change filer folder	29	change_filerfolder
91	Can delete filer folder	29	delete_filerfolder
92	Can add filer link plugin	30	add_filerlinkplugin
93	Can change filer link plugin	30	change_filerlinkplugin
94	Can delete filer link plugin	30	delete_filerlinkplugin
95	Can add filer teaser	31	add_filerteaser
96	Can change filer teaser	31	change_filerteaser
97	Can delete filer teaser	31	delete_filerteaser
98	Can add filer video	32	add_filervideo
99	Can change filer video	32	change_filervideo
100	Can delete filer video	32	delete_filervideo
101	Can add revision	33	add_revision
102	Can change revision	33	change_revision
103	Can delete revision	33	delete_revision
104	Can add version	34	add_version
105	Can change version	34	change_version
106	Can delete version	34	delete_version
107	Can add text	35	add_text
108	Can change text	35	change_text
109	Can delete text	35	delete_text
110	Can add Folder	36	add_folder
111	Can change Folder	36	change_folder
112	Can delete Folder	36	delete_folder
113	Can use directory listing	36	can_use_directory_listing
114	Can add folder permission	37	add_folderpermission
115	Can change folder permission	37	change_folderpermission
116	Can delete folder permission	37	delete_folderpermission
117	Can add file	38	add_file
118	Can change file	38	change_file
119	Can delete file	38	delete_file
120	Can add clipboard	39	add_clipboard
121	Can change clipboard	39	change_clipboard
122	Can delete clipboard	39	delete_clipboard
123	Can add clipboard item	40	add_clipboarditem
124	Can change clipboard item	40	change_clipboarditem
125	Can delete clipboard item	40	delete_clipboarditem
126	Can add image	41	add_image
127	Can change image	41	change_image
128	Can delete image	41	delete_image
129	Can add source	42	add_source
130	Can change source	42	change_source
131	Can delete source	42	delete_source
132	Can add thumbnail	43	add_thumbnail
133	Can change thumbnail	43	change_thumbnail
134	Can delete thumbnail	43	delete_thumbnail
135	Can add thumbnail dimensions	44	add_thumbnaildimensions
136	Can change thumbnail dimensions	44	change_thumbnaildimensions
137	Can delete thumbnail dimensions	44	delete_thumbnaildimensions
138	Can add filer image	45	add_filerimage
139	Can change filer image	45	change_filerimage
140	Can delete filer image	45	delete_filerimage
141	Can add thumbnail option	46	add_thumbnailoption
142	Can change thumbnail option	46	change_thumbnailoption
143	Can delete thumbnail option	46	delete_thumbnailoption
144	Can add Tag	47	add_tag
145	Can change Tag	47	change_tag
146	Can delete Tag	47	delete_tag
147	Can add Tagged Item	48	add_taggeditem
148	Can change Tagged Item	48	change_taggeditem
149	Can delete Tagged Item	48	delete_taggeditem
150	Can add key map	49	add_keymap
151	Can change key map	49	change_keymap
152	Can delete key map	49	delete_keymap
153	Can add blog category	51	add_blogcategory
154	Can change blog category	51	change_blogcategory
155	Can delete blog category	51	delete_blogcategory
156	Can add blog article	53	add_post
157	Can change blog article	53	change_post
158	Can delete blog article	53	delete_post
159	Can add latest posts plugin	54	add_latestpostsplugin
160	Can change latest posts plugin	54	change_latestpostsplugin
161	Can delete latest posts plugin	54	delete_latestpostsplugin
162	Can add author entries plugin	55	add_authorentriesplugin
163	Can change author entries plugin	55	change_authorentriesplugin
164	Can delete author entries plugin	55	delete_authorentriesplugin
165	Can add ungleich page	56	add_ungleichpage
166	Can change ungleich page	56	change_ungleichpage
167	Can delete ungleich page	56	delete_ungleichpage
168	Can add rails beta user	57	add_railsbetauser
169	Can change rails beta user	57	change_railsbetauser
170	Can delete rails beta user	57	delete_railsbetauser
171	Can add message	58	add_message
172	Can change message	58	change_message
173	Can delete message	58	delete_message
174	Can add Page meta info (all languages)	59	add_pagemeta
175	Can change Page meta info (all languages)	59	change_pagemeta
176	Can delete Page meta info (all languages)	59	delete_pagemeta
177	Can add Page meta info (language-dependent)	60	add_titlemeta
178	Can change Page meta info (language-dependent)	60	change_titlemeta
179	Can delete Page meta info (language-dependent)	60	delete_titlemeta
180	Can add rails beta user	62	add_railsbetauser
181	Can change rails beta user	62	change_railsbetauser
182	Can delete rails beta user	62	delete_railsbetauser
183	Can add supporter	63	add_supporter
184	Can change supporter	63	change_supporter
185	Can delete supporter	63	delete_supporter
186	Can add dg gallery	61	add_dggallery
187	Can change dg gallery	61	change_dggallery
188	Can delete dg gallery	61	delete_dggallery
189	Can add dg picture	64	add_dgpicture
190	Can change dg picture	64	change_dgpicture
191	Can delete dg picture	64	delete_dgpicture
192	Can add dg gallery plugin	65	add_dggalleryplugin
193	Can change dg gallery plugin	65	change_dggalleryplugin
194	Can delete dg gallery plugin	65	delete_dggalleryplugin
195	Can add dg supporters plugin	66	add_dgsupportersplugin
196	Can change dg supporters plugin	66	change_dgsupportersplugin
197	Can delete dg supporters plugin	66	delete_dgsupportersplugin
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('auth_permission_id_seq', 197, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: app
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
2	pbkdf2_sha256$15000$E4aOwgpuNSUy$ieeVxRVFCmC8zZKM3HqQJS7aug6aR7cvLKjue5mDiWs=	2015-06-13 15:22:13+02	t	sanghee	Sanghee	Kim	sanghee.kim@ungleich.ch	t	t	2015-06-13 15:22:13+02
3	pbkdf2_sha256$15000$LAd0VLScS9wH$Eo11OsKUhRwU0FITHREHDY3CaqhDmdtec+1pqYi/NTM=	2015-07-18 13:31:35.526078+02	t	nico	Nico	Schottelius	nico.schottelius@ungleich.ch	t	t	2015-06-13 15:22:45+02
4	pbkdf2_sha256$15000$DCCdqJXbFnGz$6PW2+FcxregzLA9pOShlJgY5EyiV+XeSwA3RRNYLX7A=	2015-10-29 19:07:01.570837+01	f	rscnt				f	t	2015-10-29 19:07:01.570875+01
1	pbkdf2_sha256$15000$EEGheVZj8bac$EmhJJGLebseAsKhay6p5/yJpKSsKU8u/gcFxUNujuBw=	2016-02-08 10:05:12.701267+01	t	ungleich			team@ungleich.ch	t	t	2015-06-12 18:49:33.596112+02
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: app
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('auth_user_id_seq', 4, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: app
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: cms_aliaspluginmodel; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_aliaspluginmodel (cmsplugin_ptr_id, plugin_id, alias_placeholder_id) FROM stdin;
\.


--
-- Data for Name: cms_cmsplugin; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_cmsplugin (id, "position", language, plugin_type, creation_date, changed_date, parent_id, placeholder_id, depth, numchild, path) FROM stdin;
26	2	en-us	FilerLinkPlugin	2015-06-15 15:46:46.817737+02	2015-06-15 15:46:49.750618+02	21	12	2	0	00090003
27	3	en-us	FilerLinkPlugin	2015-06-15 15:47:13.777197+02	2015-06-15 15:47:16.894176+02	21	12	2	0	00090004
14	0	en-us	FilerLinkPlugin	2015-06-13 19:51:58.005466+02	2015-06-13 19:52:11.876651+02	13	11	2	0	00060001
44	2	en-us	FilerLinkPlugin	2015-06-16 22:27:50.389155+02	2015-06-16 22:28:03.458509+02	41	14	2	0	000C0003
29	5	en-us	FilerLinkPlugin	2015-06-15 15:50:48.437019+02	2015-06-15 15:50:51.257944+02	21	12	2	0	00090006
64	2	en-us	FilerLinkPlugin	2015-07-20 21:30:44.212912+02	2015-07-20 21:30:48.353798+02	61	18	2	0	000F0003
30	6	en-us	FilerLinkPlugin	2015-06-15 15:51:33.387763+02	2015-06-15 15:51:36.855665+02	21	12	2	0	00090007
45	3	en-us	FilerLinkPlugin	2015-06-16 22:28:36.269318+02	2015-06-16 22:28:58.767315+02	41	14	2	0	000C0004
31	7	en-us	FilerLinkPlugin	2015-06-15 15:51:57.676414+02	2015-06-15 15:52:00.825409+02	21	12	2	0	00090008
8	0	en-us	FilerLinkPlugin	2015-06-12 22:33:35.572452+02	2015-06-12 22:34:25.8933+02	6	7	2	0	00040001
32	8	en-us	FilerLinkPlugin	2015-06-15 15:52:15.269583+02	2015-06-15 15:52:18.496+02	21	12	2	0	00090009
49	6	en-us	FilerImagePlugin	2015-06-16 23:15:54.671685+02	2015-06-16 23:19:53.133018+02	41	14	2	0	000C0008
6	0	en-us	TextPlugin	2015-06-12 21:58:50.169957+02	2015-06-12 23:04:36.831752+02	\N	7	1	1	0004
33	9	en-us	FilerLinkPlugin	2015-06-15 15:52:39.176543+02	2015-06-15 15:52:44.554555+02	21	12	2	0	0009000A
13	0	en-us	TextPlugin	2015-06-13 19:47:15.784346+02	2015-06-14 06:46:11.774696+02	\N	11	1	4	0006
9	0	en-us	FilerImagePlugin	2015-06-12 23:10:09.310396+02	2015-06-12 23:10:09.319275+02	4	9	2	0	00030001
4	0	en-us	TextPlugin	2015-06-12 19:54:49.162118+02	2015-06-12 23:06:53.345931+02	\N	9	1	1	0003
17	1	en-us	FilerImagePlugin	2015-06-14 06:43:51.755039+02	2015-06-14 06:46:11.833131+02	13	11	2	0	00060003
18	2	en-us	FilerImagePlugin	2015-06-14 06:44:09.869605+02	2015-06-14 06:46:11.842905+02	13	11	2	0	00060004
19	3	en-us	FilerImagePlugin	2015-06-14 06:44:22.081435+02	2015-06-14 06:46:11.852445+02	13	11	2	0	00060005
20	0	en-us	TextPlugin	2015-06-14 07:11:57.14237+02	2015-06-14 07:11:57.314821+02	\N	10	1	0	0008
46	4	en-us	FilerLinkPlugin	2015-06-16 22:33:58.086631+02	2015-06-16 22:34:01.279322+02	41	14	2	0	000C0005
34	10	en-us	FilerLinkPlugin	2015-06-15 15:52:59.217126+02	2015-06-15 15:53:01.666042+02	21	12	2	0	0009000B
50	7	en-us	FilerImagePlugin	2015-06-16 23:17:01.340229+02	2015-06-16 23:19:53.142557+02	41	14	2	0	000C0009
51	8	en-us	FilerImagePlugin	2015-06-16 23:17:51.462657+02	2015-06-16 23:19:53.152077+02	41	14	2	0	000C000A
67	1	en-us	FilerLinkPlugin	2015-07-27 00:47:45.188355+02	2015-07-27 00:48:20.01272+02	65	19	2	0	000G0002
52	9	en-us	FilerImagePlugin	2015-06-16 23:18:41.569576+02	2015-06-16 23:20:16.720179+02	41	14	2	0	000C000B
24	0	en-us	FilerLinkPlugin	2015-06-14 23:37:56.549604+02	2015-06-14 23:38:27.668868+02	21	12	2	0	00090001
38	0	en-us	FilerImagePlugin	2015-06-15 22:12:38.592686+02	2015-06-15 22:24:16.70615+02	22	13	2	0	000A0003
1	0	en-us	TextPlugin	2015-06-12 18:53:05.418334+02	2015-06-15 15:57:00.887099+02	\N	2	1	0	0001
25	1	en-us	FilerLinkPlugin	2015-06-15 00:02:41.481822+02	2015-06-15 00:02:51.619338+02	21	12	2	0	00090002
39	1	en-us	FilerImagePlugin	2015-06-15 22:12:59.845088+02	2015-06-15 22:24:16.716705+02	22	13	2	0	000A0004
40	2	en-us	FilerImagePlugin	2015-06-15 22:23:41.774831+02	2015-06-15 22:24:16.727631+02	22	13	2	0	000A0005
47	5	en-us	FilerLinkPlugin	2015-06-16 22:47:38.009169+02	2015-06-16 22:47:46.891696+02	41	14	2	0	000C0006
28	4	en-us	FilerLinkPlugin	2015-06-15 15:47:55.647303+02	2015-06-15 16:06:02.531631+02	21	12	2	0	00090005
41	0	en-us	TextPlugin	2015-06-16 22:14:04.282513+02	2015-06-16 23:20:21.669854+02	\N	14	1	10	000C
53	0	en-us	TextPlugin	2015-06-21 10:31:55.480776+02	2015-06-22 23:56:08.369576+02	\N	15	1	4	000D
21	0	en-us	TextPlugin	2015-06-14 23:22:06.930688+02	2015-06-15 17:30:02.895475+02	\N	12	1	11	0009
68	2	en-us	FilerLinkPlugin	2015-07-27 01:15:03.311183+02	2015-07-27 01:15:27.731662+02	65	19	2	0	000G0003
22	0	en-us	TextPlugin	2015-06-14 23:24:27.724016+02	2015-06-15 22:38:14.86652+02	\N	13	1	3	000A
59	0	en-us	TextPlugin	2015-06-26 11:45:50.300563+02	2015-06-26 11:45:50.460937+02	\N	16	1	1	000E
55	0	en-us	FilerImagePlugin	2015-06-22 15:39:11.56687+02	2015-06-22 23:29:11.992851+02	53	15	2	0	000D0001
42	0	en-us	FilerLinkPlugin	2015-06-16 22:17:27.55228+02	2015-06-16 22:17:37.61838+02	41	14	2	0	000C0001
56	1	en-us	FilerImagePlugin	2015-06-22 23:20:35.790788+02	2015-06-22 23:29:19.787657+02	53	15	2	0	000D0002
43	1	en-us	FilerLinkPlugin	2015-06-16 22:22:32.166113+02	2015-06-16 22:22:36.349296+02	41	14	2	0	000C0002
57	2	en-us	FilerImagePlugin	2015-06-22 23:28:15.995528+02	2015-06-22 23:29:27.840494+02	53	15	2	0	000D0003
60	0	en-us	FilerLinkPlugin	2015-06-26 11:47:07.129332+02	2015-06-26 11:47:11.833642+02	59	16	2	0	000E0001
61	0	en-us	TextPlugin	2015-07-20 21:15:27.714523+02	2015-07-20 21:31:59.07523+02	\N	18	1	3	000F
58	3	en-us	FilerLinkPlugin	2015-06-22 23:37:33.698877+02	2015-06-22 23:37:45.17474+02	53	15	2	0	000D0004
62	0	en-us	FilerLinkPlugin	2015-07-20 21:17:28.199265+02	2015-07-20 21:17:35.893519+02	61	18	2	0	000F0001
69	3	en-us	FilerLinkPlugin	2015-07-27 01:37:32.062729+02	2015-07-27 01:37:36.078352+02	65	19	2	0	000G0004
63	1	en-us	FilerLinkPlugin	2015-07-20 21:20:11.650034+02	2015-07-20 21:20:15.208989+02	61	18	2	0	000F0002
70	4	en-us	FilerLinkPlugin	2015-07-27 01:37:46.86029+02	2015-07-27 01:37:49.867409+02	65	19	2	0	000G0005
66	0	en-us	FilerLinkPlugin	2015-07-27 00:47:27.322604+02	2015-07-27 00:47:32.134591+02	65	19	2	0	000G0001
76	0	en-us	CMSGalleryPlugin	2016-02-08 10:37:50.103497+01	2016-02-08 10:37:56.601433+01	\N	112	1	0	000L
65	0	en-us	TextPlugin	2015-07-27 00:38:45.141585+02	2015-09-27 01:02:08.613307+02	\N	19	1	5	000G
77	0	en-us	CMSGalleryPlugin	2016-02-08 10:37:50.103497+01	2016-02-08 10:38:02.184136+01	\N	111	1	0	000M
74	0	en-us	TextPlugin	2015-06-12 18:53:05.418334+02	2015-11-05 08:34:37.061213+01	\N	3	1	0	000K
72	0	de	TextPlugin	2015-11-05 08:30:30.341081+01	2015-11-05 08:30:30.540286+01	\N	2	1	0	000I
75	0	en-us	FilerLinkPlugin	2015-11-05 08:36:03.319748+01	2015-11-05 08:36:11.144646+01	71	20	2	0	000H0001
73	0	de	TextPlugin	2015-11-05 08:30:48.470739+01	2015-11-05 08:30:48.529083+01	\N	19	1	0	000J
71	0	en-us	TextPlugin	2015-09-29 21:07:32.182438+02	2015-11-05 08:36:13.808623+01	\N	20	1	1	000H
\.


--
-- Name: cms_cmsplugin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_cmsplugin_id_seq', 77, true);


--
-- Data for Name: cms_globalpagepermission; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_globalpagepermission (id, can_change, can_add, can_delete, can_change_advanced_settings, can_publish, can_change_permissions, can_move_page, can_view, can_recover_page, group_id, user_id) FROM stdin;
\.


--
-- Name: cms_globalpagepermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_globalpagepermission_id_seq', 1, false);


--
-- Data for Name: cms_globalpagepermission_sites; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_globalpagepermission_sites (id, globalpagepermission_id, site_id) FROM stdin;
\.


--
-- Name: cms_globalpagepermission_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_globalpagepermission_sites_id_seq', 1, false);


--
-- Data for Name: cms_page; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_page (id, created_by, changed_by, creation_date, changed_date, publication_date, publication_end_date, in_navigation, soft_root, reverse_id, navigation_extenders, template, login_required, limit_visibility_in_menu, is_home, application_urls, application_namespace, publisher_is_draft, languages, revision_id, xframe_options, parent_id, publisher_public_id, site_id, depth, numchild, path) FROM stdin;
5	ungleich	ungleich	2015-10-04 18:27:41.288458+02	2016-02-08 10:38:02.293016+01	2015-10-04 18:47:36.159972+02	\N	t	t	\N		cms/digitalglarus/index.html	f	\N	f		\N	t	en-us	0	0	\N	7	1	1	2	0005
10	ungleich	ungleich	2015-10-04 23:27:23.422668+02	2015-10-04 23:27:23.548473+02	2015-10-04 23:27:23.416582+02	\N	t	f	\N	\N	INHERIT	f	\N	f	\N	\N	f	en-us	0	0	7	8	1	2	0	00060001
8	ungleich	ungleich	2015-10-04 23:22:33.837413+02	2015-10-04 23:27:23.683172+02	2015-10-04 23:27:23.416582+02	\N	t	f	\N	\N	INHERIT	f	\N	f	\N	\N	t	en-us	0	0	5	10	1	2	0	00050001
13	ungleich	ungleich	2016-02-08 10:40:46.348539+01	2016-02-08 10:40:46.426704+01	2016-02-08 10:40:46.34208+01	\N	t	f	\N		INHERIT	f	\N	f		\N	f	en-us	0	0	\N	12	1	1	0	0008
4	ungleich	ungleich	2015-06-12 19:17:49.270519+02	2016-02-08 10:40:46.439092+01	2015-06-12 19:17:49.261484+02	\N	t	f	\N		cms/ungleichch/blog.html	f	\N	t	BlogApp	djangocms_blog	f	en-us	0	0	\N	3	1	1	0	0004
11	ungleich	ungleich	2015-10-04 23:27:56.750131+02	2015-10-04 23:27:56.813439+02	2015-10-04 23:27:56.742409+02	\N	t	f	\N	\N	INHERIT	f	\N	f	\N	\N	f	en-us	0	0	7	9	1	2	0	00060002
9	ungleich	ungleich	2015-10-04 23:22:53.644941+02	2015-10-04 23:27:56.858727+02	2015-10-04 23:27:56.742409+02	\N	t	f	\N	\N	INHERIT	f	\N	f	\N	\N	t	en-us	0	0	5	11	1	2	0	00050002
12	ungleich	ungleich	2016-02-08 10:38:35.737286+01	2016-02-08 10:40:46.509664+01	2016-02-08 10:40:46.34208+01	\N	t	f	\N		INHERIT	f	\N	f		\N	t	en-us	0	0	\N	13	1	1	0	0007
3	ungleich	ungleich	2015-06-12 19:05:57.028042+02	2016-02-08 10:40:46.52186+01	2015-06-12 19:17:49.261484+02	\N	t	f	\N		cms/ungleichch/blog.html	f	\N	t	BlogApp	djangocms_blog	t	en-us,de	0	0	\N	4	1	1	0	0003
7	ungleich	ungleich	2015-10-04 18:47:36.16583+02	2016-02-08 10:38:02.189014+01	2015-10-04 18:47:36.159972+02	\N	t	t	\N		cms/digitalglarus/index.html	f	\N	f		\N	f	en-us	0	0	\N	5	1	1	2	0006
\.


--
-- Name: cms_page_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_page_id_seq', 13, true);


--
-- Data for Name: cms_page_placeholders; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_page_placeholders (id, page_id, placeholder_id) FROM stdin;
3	3	6
4	4	8
5	5	21
6	5	22
7	5	23
8	5	24
9	5	25
10	5	26
11	5	27
12	5	28
13	5	29
23	7	39
24	7	40
25	7	41
26	7	42
27	7	43
28	7	44
29	7	45
30	7	46
31	7	47
41	8	57
42	8	58
43	8	59
44	8	60
45	8	61
46	8	62
47	8	63
48	8	64
49	8	65
50	10	66
51	10	67
52	10	68
53	10	69
54	10	70
55	10	71
56	10	72
57	10	73
58	10	74
59	10	75
60	10	76
61	10	77
62	10	78
63	10	79
64	10	80
65	9	81
66	9	82
67	9	83
68	9	84
69	9	85
70	9	86
71	9	87
72	9	88
73	9	89
74	11	90
75	11	91
76	11	92
77	11	93
78	11	94
79	11	95
80	11	96
81	11	97
82	11	98
95	7	111
96	5	112
97	12	113
98	12	114
99	12	115
100	12	116
101	12	117
102	13	118
103	13	119
104	13	120
105	13	121
106	13	122
\.


--
-- Name: cms_page_placeholders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_page_placeholders_id_seq', 106, true);


--
-- Data for Name: cms_pagepermission; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_pagepermission (id, can_change, can_add, can_delete, can_change_advanced_settings, can_publish, can_change_permissions, can_move_page, can_view, grant_on, group_id, page_id, user_id) FROM stdin;
\.


--
-- Name: cms_pagepermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_pagepermission_id_seq', 1, false);


--
-- Data for Name: cms_pageuser; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_pageuser (user_ptr_id, created_by_id) FROM stdin;
\.


--
-- Data for Name: cms_pageusergroup; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_pageusergroup (group_ptr_id, created_by_id) FROM stdin;
\.


--
-- Data for Name: cms_placeholder; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_placeholder (id, slot, default_width) FROM stdin;
1	clipboard	\N
2	footer_copyright	\N
3	footer_copyright	\N
6	page_content	\N
7	post_content	\N
8	page_content	\N
9	post_content	\N
10	post_content	\N
11	post_content	\N
12	post_content	\N
13	post_content	\N
14	post_content	\N
15	post_content	\N
16	post_content	\N
17	clipboard	\N
18	post_content	\N
19	post_content	\N
20	post_content	\N
21	digital_glarus_build_a_tech_valley	\N
22	digital_glarus_build_a_tech_valley_content	\N
23	digital_glarus_a_new_area	\N
24	digital_glarus_a_new_area_content	\N
25	digital_glarus_why_be_interested	\N
26	digital_glarus_why_be_interested_content	\N
27	digital_glarus_where_we_are	\N
28	digital_glarus_where_we_are_content	\N
29	digital_glarus_legend	\N
39	digital_glarus_build_a_tech_valley	\N
40	digital_glarus_build_a_tech_valley_content	\N
41	digital_glarus_a_new_area	\N
42	digital_glarus_a_new_area_content	\N
43	digital_glarus_why_be_interested	\N
44	digital_glarus_why_be_interested_content	\N
45	digital_glarus_where_we_are	\N
46	digital_glarus_where_we_are_content	\N
47	digital_glarus_legend	\N
57	digital_glarus_build_a_tech_valley	\N
58	digital_glarus_build_a_tech_valley_content	\N
59	digital_glarus_a_new_area	\N
60	digital_glarus_a_new_area_content	\N
61	digital_glarus_why_be_interested	\N
62	digital_glarus_why_be_interested_content	\N
63	digital_glarus_where_we_are	\N
64	digital_glarus_where_we_are_content	\N
65	digital_glarus_legend	\N
66	digitalglarus_why_us	\N
67	digitalglarus_why_us_content	\N
68	digitalglarus_why_glarus	\N
69	digitalglarus_why_glarus_beautiful_landscape	\N
70	digitalglarus_why_glarus_affordable_price	\N
71	digitalglarus_why_glarus_direct_connection_zurich	\N
72	digital_glarus_legend	\N
73	digital_glarus_build_a_tech_valley	\N
74	digital_glarus_build_a_tech_valley_content	\N
75	digital_glarus_a_new_area	\N
76	digital_glarus_a_new_area_content	\N
77	digital_glarus_why_be_interested	\N
78	digital_glarus_why_be_interested_content	\N
79	digital_glarus_where_we_are	\N
80	digital_glarus_where_we_are_content	\N
81	digital_glarus_build_a_tech_valley	\N
82	digital_glarus_build_a_tech_valley_content	\N
83	digital_glarus_a_new_area	\N
84	digital_glarus_a_new_area_content	\N
85	digital_glarus_why_be_interested	\N
86	digital_glarus_why_be_interested_content	\N
87	digital_glarus_where_we_are	\N
88	digital_glarus_where_we_are_content	\N
89	digital_glarus_legend	\N
90	digital_glarus_build_a_tech_valley	\N
91	digital_glarus_build_a_tech_valley_content	\N
92	digital_glarus_a_new_area	\N
93	digital_glarus_a_new_area_content	\N
94	digital_glarus_why_be_interested	\N
95	digital_glarus_why_be_interested_content	\N
96	digital_glarus_where_we_are	\N
97	digital_glarus_where_we_are_content	\N
98	digital_glarus_legend	\N
111	digital_glarus_gallery_grid	\N
112	digital_glarus_gallery_grid	\N
113	digitalglarus_why_glarus	\N
114	digitalglarus_why_glarus_beautiful_landscape	\N
115	digitalglarus_why_glarus_affordable_price	\N
116	digitalglarus_why_glarus_direct_connection_zurich	\N
117	digital_glarus_legend	\N
118	digitalglarus_why_glarus	\N
119	digitalglarus_why_glarus_beautiful_landscape	\N
120	digitalglarus_why_glarus_affordable_price	\N
121	digitalglarus_why_glarus_direct_connection_zurich	\N
122	digital_glarus_legend	\N
\.


--
-- Name: cms_placeholder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_placeholder_id_seq', 122, true);


--
-- Data for Name: cms_placeholderreference; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_placeholderreference (cmsplugin_ptr_id, name, placeholder_ref_id) FROM stdin;
\.


--
-- Data for Name: cms_staticplaceholder; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_staticplaceholder (id, name, code, dirty, creation_method, draft_id, public_id, site_id) FROM stdin;
1	footer_copyright	footer_copyright	f	template	2	3	\N
\.


--
-- Name: cms_staticplaceholder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_staticplaceholder_id_seq', 1, true);


--
-- Data for Name: cms_title; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_title (id, language, title, page_title, menu_title, meta_description, slug, path, has_url_overwrite, redirect, creation_date, published, publisher_is_draft, publisher_state, page_id, publisher_public_id) FROM stdin;
11	de	blog	blog	blog	blog\r\n	blog		f	\N	2015-11-05 08:30:25.866437+01	f	t	1	3	\N
4	en-us	Blog	ungleich Blog	Blog	on OpenSource, technology, our passion and interests...	blog		f		2015-06-12 19:05:57.066362+02	t	f	0	4	3
3	en-us	Blog	ungleich Blog	Blog	on OpenSource, technology, our passion and interests...	blog		f		2015-06-12 19:05:57.066362+02	t	t	0	3	4
9	en-us	fooffff	ffff	ffff	ffffff	fooffff	digitalglarus/fooffff	f	\N	2015-10-04 23:22:33.989754+02	t	f	0	10	7
10	en-us	ccccccccccccc	ccccccccccccccccc	cccccccccccccc	ccc	ccccccccccccc	digitalglarus/ccccccccccccc	f	\N	2015-10-04 23:22:53.668087+02	t	f	0	11	8
6	en-us	digital glarus home	Digital Glarus	home		digital-glarus-home	digitalglarus	t		2015-10-04 18:27:41.449183+02	t	f	0	7	5
5	en-us	digital glarus home	Digital Glarus	home		digital-glarus-home	digitalglarus	t		2015-10-04 18:27:41.449183+02	t	t	0	5	6
13	en-us	supporters	supporters	supporters		supporters	supporters	f		2016-02-08 10:38:35.910169+01	t	f	0	13	12
12	en-us	supporters	supporters	supporters		supporters	supporters	f		2016-02-08 10:38:35.910169+01	t	t	0	12	13
7	en-us	fooffff	ffff	ffff	ffffff	fooffff	digitalglarus/fooffff	f	\N	2015-10-04 23:22:33.989754+02	t	t	0	8	9
8	en-us	ccccccccccccc	ccccccccccccccccc	cccccccccccccc	ccc	ccccccccccccc	digitalglarus/ccccccccccccc	f	\N	2015-10-04 23:22:53.668087+02	t	t	0	9	10
\.


--
-- Name: cms_title_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_title_id_seq', 13, true);


--
-- Data for Name: cms_usersettings; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_usersettings (id, language, clipboard_id, user_id) FROM stdin;
1	en-us	1	1
2	en-us	17	3
\.


--
-- Name: cms_usersettings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_usersettings_id_seq', 2, true);


--
-- Data for Name: cmsplugin_filer_file_filerfile; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_file_filerfile (cmsplugin_ptr_id, title, target_blank, style, file_id) FROM stdin;
\.


--
-- Data for Name: cmsplugin_filer_folder_filerfolder; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_folder_filerfolder (cmsplugin_ptr_id, title, style, folder_id) FROM stdin;
\.


--
-- Data for Name: cmsplugin_filer_image_filerimage; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_image_filerimage (cmsplugin_ptr_id, style, caption_text, image_url, alt_text, use_original_image, use_autoscale, width, height, crop, upscale, alignment, free_link, original_link, description, target_blank, file_link_id, image_id, page_link_id, thumbnail_option_id) FROM stdin;
17					f	f	\N	\N	t	t	\N		f		f	\N	13	\N	\N
18					f	f	\N	\N	t	t	\N		f		f	\N	11	\N	\N
19					f	f	\N	\N	t	t	\N		f		f	\N	12	\N	\N
38					f	f	\N	\N	t	t	\N		f		f	\N	19	\N	\N
39					f	f	\N	\N	t	t	\N		f		f	\N	21	\N	\N
40					f	f	\N	\N	t	t	\N		f		f	\N	22	\N	\N
49					f	f	\N	\N	t	t	\N		f		f	\N	24	\N	\N
50					f	f	\N	\N	t	t	\N		f		f	\N	25	\N	\N
51					f	f	\N	\N	t	t	\N		f		f	\N	26	\N	\N
52					f	f	\N	\N	t	t	\N		f		f	\N	27	\N	\N
55					f	f	\N	\N	t	t	\N		f		f	\N	29	\N	\N
56					f	f	\N	\N	t	t	\N		f		f	\N	30	\N	\N
57					f	f	\N	\N	t	t	\N		f		f	\N	31	\N	\N
\.


--
-- Data for Name: cmsplugin_filer_image_thumbnailoption; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_image_thumbnailoption (id, name, width, height, crop, upscale) FROM stdin;
\.


--
-- Name: cmsplugin_filer_image_thumbnailoption_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cmsplugin_filer_image_thumbnailoption_id_seq', 1, false);


--
-- Data for Name: cmsplugin_filer_link_filerlinkplugin; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_link_filerlinkplugin (cmsplugin_ptr_id, name, url, mailto, link_style, new_window, file_id, page_link_id) FROM stdin;
8	DjangoCMS blog	https://github.com/nephila/djangocms-blog		 	t	\N	\N
14	OpenNebulaConf 2015.	http://2015.opennebulaconf.com/		 	t	\N	\N
24	rails-hosting.ch	http://rails-hosting.ch		 	t	\N	\N
25	OpenNebula	http://opennebula.org		 	f	\N	\N
26	Ceph	http://ceph.com/		 	f	\N	\N
27	GlusterFS	http://www.gluster.org/		 	f	\N	\N
29	Nginx	http://nginx.org/		 	f	\N	\N
30	PostgreSQL	https://www.postgresql.org/		 	f	\N	\N
31	DjangoCMS Blog	https://github.com/nephila/djangocms-blog		 	f	\N	\N
32	DjangoCMS	http://django-cms.org/		 	f	\N	\N
33	uwsgi	http://uwsgi-docs.readthedocs.org/en/latest/		 	f	\N	\N
34	Django	https://www.djangoproject.com/		 	f	\N	\N
28	cdist	http://www.nico.schottelius.org/software/cdist/		 	f	\N	\N
42	OpenCloudDay 2015 in Bern	http://ch-open.ch/events/aktuelle-events/160615-open-cloud-day-2015/		 	f	\N	\N
43	@Jens	https://twitter.com/jcfischer		 	f	\N	\N
44	Digital Glarus	https://digitalglarus.ungleich.ch		 	f	\N	\N
45	follow us on Twitter	https://twitter.com/ungleich		 	f	\N	\N
46	/ch/open	http://www.ch-open.ch/		 	f	\N	\N
47	@ICCLab	https://twitter.com/icc_lab		 	f	\N	\N
58	Digital Glarus	https://digitalglarus.ungleich.ch		 	f	\N	\N
60	PostgreSQL Europe	https://www.postgresql.eu/		 	f	\N	\N
62	Digital Glarus	https://digitalglarus.ungleich.ch		 	f	\N	\N
63	Makers im Zigerschlitz	http://www.meetup.com/Makers-im-Zigerschlitz/events/223111211/		 	f	\N	\N
64	follow us on Twitter	https://twitter.com/ungleich		 	f	\N	\N
66	Co-Working Space	https://en.wikipedia.org/wiki/Coworking		 	f	\N	\N
67	Digital Glarus	https://digitalglarus.ungleich.ch/		 	f	\N	\N
68	@ungleich	https://twitter.com/ungleich		 	f	\N	\N
69	fill out the form	https://docs.google.com/forms/d/1S2pQ2LDdRi2zbYHeBlusR5SoQjFy0HlHPTKgNKYIGak/viewform?usp=send_form		 	f	\N	\N
70	fill out the project form	https://docs.google.com/forms/d/1S2pQ2LDdRi2zbYHeBlusR5SoQjFy0HlHPTKgNKYIGak/viewform?usp=send_form		 	f	\N	\N
75	testing text	https://medium.com/google-developers/exploring-es7-decorators-76ecb65fb841		 	f	\N	\N
\.


--
-- Data for Name: cmsplugin_filer_teaser_filerteaser; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_teaser_filerteaser (cmsplugin_ptr_id, title, image_url, style, use_autoscale, width, height, free_link, description, target_blank, image_id, page_link_id) FROM stdin;
\.


--
-- Data for Name: cmsplugin_filer_video_filervideo; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_video_filervideo (cmsplugin_ptr_id, movie_url, width, height, auto_play, auto_hide, fullscreen, loop, bgcolor, textcolor, seekbarcolor, seekbarbgcolor, loadingbarcolor, buttonoutcolor, buttonovercolor, buttonhighlightcolor, image_id, movie_id) FROM stdin;
\.


--
-- Data for Name: digitalglarus_dggallery; Type: TABLE DATA; Schema: public; Owner: app
--

COPY digitalglarus_dggallery (id, name, parent_id) FROM stdin;
1	Home Gallery	\N
\.


--
-- Name: digitalglarus_dggallery_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('digitalglarus_dggallery_id_seq', 1, true);


--
-- Data for Name: digitalglarus_dggalleryplugin; Type: TABLE DATA; Schema: public; Owner: app
--

COPY digitalglarus_dggalleryplugin (cmsplugin_ptr_id, "dgGallery_id") FROM stdin;
76	1
77	1
\.


--
-- Data for Name: digitalglarus_dgpicture; Type: TABLE DATA; Schema: public; Owner: app
--

COPY digitalglarus_dgpicture (id, description, gallery_id, image_id) FROM stdin;
1	ungleich	1	37
2	dg	1	36
3	dg	1	38
\.


--
-- Name: digitalglarus_dgpicture_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('digitalglarus_dgpicture_id_seq', 3, true);


--
-- Data for Name: digitalglarus_dgsupportersplugin; Type: TABLE DATA; Schema: public; Owner: app
--

COPY digitalglarus_dgsupportersplugin (cmsplugin_ptr_id) FROM stdin;
\.


--
-- Data for Name: digitalglarus_message; Type: TABLE DATA; Schema: public; Owner: app
--

COPY digitalglarus_message (id, name, email, phone_number, message, received_date) FROM stdin;
\.


--
-- Name: digitalglarus_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('digitalglarus_message_id_seq', 1, false);


--
-- Data for Name: digitalglarus_supporter; Type: TABLE DATA; Schema: public; Owner: app
--

COPY digitalglarus_supporter (id, name, description) FROM stdin;
\.


--
-- Name: digitalglarus_supporter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('digitalglarus_supporter_id_seq', 1, false);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: app
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
1	2015-06-12 18:53:01.623776+02	1	Home	1		11	1
2	2015-06-12 19:05:57.105218+02	3	Blog	1		11	1
3	2015-06-12 19:06:25.68614+02	3	Blog	2	Changed application_urls, application_namespace and xframe_options.	11	1
4	2015-06-12 19:07:21.654196+02	1	announcement	1		51	1
5	2015-06-12 19:10:34.583595+02	1	ungleich Blog launched	1		53	1
6	2015-06-12 19:14:13.032533+02	3	Blog	2	Changed template and xframe_options.	11	1
7	2015-06-12 19:14:40.886446+02	1	ungleich blog launched	2	Changed title and tags.	53	1
8	2015-06-12 19:17:49.46888+02	3	Blog	2		11	1
9	2015-06-12 19:21:50.285698+02	2	opennebula	1		51	1
10	2015-06-12 19:23:37.226156+02	2	OpenNebulaConf 2015	1		53	1
11	2015-06-12 19:24:42.572774+02	1	ungleich.ch	2	Changed domain and name.	7	1
12	2015-06-12 19:25:07.868424+02	1	blog.ungleich.ch	2	Changed domain.	7	1
13	2015-06-12 19:26:30.363273+02	2	OpenNebulaConf 2015	2	Changed abstract and tags.	53	1
14	2015-06-12 19:28:56.127053+02	2	OpenNebulaConf 2015	2	Changed categories and tags.	53	1
15	2015-06-12 19:32:08.451294+02	2	OpenNebulaConf 2015	2	Changed publish and tags.	53	1
16	2015-06-12 19:35:00.637214+02	2	OpenNebulaConf 2015	2	Changed abstract and tags.	53	1
17	2015-06-12 19:49:43.82979+02	1	ungleich	2	No fields changed.	8	1
18	2015-06-12 19:55:36.291237+02	2	OpenNebulaConf 2015	2	Changed abstract and tags.	53	1
19	2015-06-12 21:55:54.701245+02	1	ungleich blog launched	2	Changed abstract and tags.	53	1
20	2015-06-12 21:57:19.415793+02	5	5	3		10	1
21	2015-06-12 21:57:33.678+02	1	ungleich	2	No fields changed.	8	1
22	2015-06-12 21:58:26.402886+02	1	ungleich blog launched	2	Changed abstract and tags.	53	1
23	2015-06-12 22:03:12.485109+02	3	Blog	2	Changed page_title.	11	1
24	2015-06-12 22:04:54.009245+02	3	Blog	2		11	1
25	2015-06-12 22:06:13.555449+02	3	Blog	2	Changed menu_title and page_title.	11	1
26	2015-06-12 22:06:55.919673+02	3	Blog	2	Changed page_title.	11	1
27	2015-06-12 22:07:32.136411+02	3	Blog	2		11	1
28	2015-06-12 22:17:24.393782+02	3	Blog	2	Changed page_title.	11	1
29	2015-06-12 22:24:27.361495+02	3	hosting	1		51	1
30	2015-06-12 22:25:21.343339+02	3	Application Hosting	1		53	1
31	2015-06-12 22:25:31.019931+02	3	Application Hosting	2	Changed tags.	53	1
32	2015-06-12 22:25:53.92103+02	3	Application Hosting	2	Changed tags and date_published.	53	1
33	2015-06-12 23:06:07.746567+02	2	OpenNebulaConf 2015	2	Changed tags and date_published.	53	1
34	2015-06-12 23:07:42.088516+02	3	Blog	2		11	1
35	2015-06-13 10:14:14.632456+02	2	OpenNebulaConf 2015	2	Changed categories and tags.	53	1
36	2015-06-13 11:27:58.111546+02	2	OpenNebulaConf 2015	3		53	1
37	2015-06-13 11:29:11.435971+02	4	 OpenNebulaConf 2015 	1		53	1
38	2015-06-13 11:29:16.09016+02	4	 OpenNebulaConf 2015 	2	Changed tags.	53	1
39	2015-06-13 11:30:48.787184+02	4	 OpenNebulaConf 2015 	2	Changed tags.	53	1
40	2015-06-13 11:32:13.135422+02	10	10	3		10	1
41	2015-06-13 15:04:06.799637+02	1	ungleich blog launched	2	Changed abstract and tags.	53	1
42	2015-06-13 15:11:03.536055+02	3	Blog	2		11	1
43	2015-06-13 15:13:17.878856+02	3	Blog	2		11	1
44	2015-06-13 15:22:13.384436+02	2	sanghee	1		4	1
45	2015-06-13 15:22:45.638851+02	3	nico	1		4	1
46	2015-06-13 15:23:05.973436+02	3	nico	2	Changed first_name, last_name, email, is_staff and is_superuser.	4	1
47	2015-06-13 15:23:25.19965+02	2	sanghee	2	Changed first_name, last_name, email, is_staff and is_superuser.	4	1
48	2015-06-13 19:37:46.061872+02	4	 OpenNebulaConf 2015 	2	Changed abstract and tags.	53	1
49	2015-06-13 19:46:50.586349+02	4	October 20-22 2015, Meet us in Barcelona!	2	Changed title, publish and tags.	53	1
50	2015-06-13 19:52:25.565082+02	3	Blog	2		11	1
51	2015-06-13 20:15:22.853187+02	1	14473379828_84376f1229_h.jpg	3		41	1
52	2015-06-13 20:22:46.173677+02	3	14473379828_84376f1229_h.jpg	2	No fields changed.	41	1
53	2015-06-13 20:22:51.892558+02	4	14473379828_84376f1229_h.jpg	3		41	1
54	2015-06-13 20:22:55.655192+02	3	14473379828_84376f1229_h.jpg	3		41	1
55	2015-06-13 20:22:59.813589+02	2	14473379828_84376f1229_h.jpg	3		41	1
56	2015-06-13 20:23:42.481738+02	6	14473379828_84376f1229_h.jpg	3		41	1
57	2015-06-14 04:53:32.803307+02	2	articles	2	Changed name.	36	1
58	2015-06-14 04:53:45.679853+02	5	14473379828_84376f1229_h.jpg	3		41	1
59	2015-06-14 05:10:32.327331+02	3	img	2	Changed name.	36	1
60	2015-06-14 05:13:23.742703+02	4	October 20-22 2015, Meet us in Barcelona!	2	Changed tags and main_image.	53	1
61	2015-06-14 05:14:35.023026+02	3	Blog	2	Changed meta_description.	11	1
62	2015-06-14 05:15:00.309542+02	3	Blog	2		11	1
63	2015-06-14 05:17:31.940109+02	14	14473379828_84376f1229_h.jpg	3		41	1
64	2015-06-14 05:17:50.419391+02	4	October 20-22 2015, Meet us in Barcelona!	2	Changed tags and main_image.	53	1
65	2015-06-14 05:42:24.173543+02	4	October 20-22 2015, Meet us in Barcelona!	2	Changed tags and sites.	53	1
66	2015-06-14 05:42:44.242971+02	1	blog.ungleich.ch	2	Changed name.	7	1
67	2015-06-14 05:43:15.804351+02	3	Blog	2	Changed xframe_options.	11	1
68	2015-06-14 05:43:22.039775+02	3	Blog	2	No fields changed.	11	1
69	2015-06-14 06:11:11.055257+02	4	October 20-22 2015, Meet us in Barcelona!	2	Changed tags.	53	1
70	2015-06-14 06:48:27.067971+02	1	UngleichPage object	1		56	1
71	2015-06-14 06:48:33.905655+02	3	Blog	2		11	1
72	2015-06-14 06:49:44.904955+02	1	ungleich blog launched	2	Changed abstract and tags.	53	1
73	2015-06-14 06:56:02.063255+02	1	ungleich blog launched	2	Changed abstract, tags and main_image.	53	1
74	2015-06-14 06:56:32.225684+02	1	ungleich blog launched	2	Changed abstract and tags.	53	1
75	2015-06-14 07:05:22.149361+02	3	Blog	2		11	1
76	2015-06-14 07:20:25.178737+02	1	https://blog.ungleich.ch	2	Changed domain.	7	1
77	2015-06-14 07:21:09.484391+02	1	blog.ungleich.ch	2	Changed domain.	7	1
78	2015-06-14 07:26:04.698325+02	1	https://blog.ungleich.ch	2	Changed domain.	7	1
79	2015-06-14 07:26:32.802673+02	1	blog.ungleich.ch	2	Changed domain.	7	1
80	2015-06-14 23:19:37.816758+02	5	Preview of the ungleich hosting technologies	1		53	1
81	2015-06-14 23:22:29.215379+02	4	technology	1		51	1
82	2015-06-14 23:22:38.10048+02	5	Preview of the ungleich hosting technologies	2	Changed categories, abstract and tags.	53	1
83	2015-06-14 23:23:32.370425+02	6	OpenNebula + Openstack + Cloudstack = Open Cloud Day Bern	1		53	1
84	2015-06-14 23:28:20.839641+02	19	opencloudday.png	2	No fields changed.	41	1
85	2015-06-14 23:54:31.800422+02	5	Preview of the ungleich hosting technologies	2	Changed abstract and tags.	53	1
166	2015-10-05 00:55:29.721747+02	5	digital glarus home	2		11	1
86	2015-06-15 15:54:14.507513+02	5	Preview of the ungleich hosting technologies	2	Changed tags and meta_keywords.	53	1
87	2015-06-15 15:54:36.288491+02	3	Blog	2		11	1
88	2015-06-15 15:57:51.794578+02	5	Preview of the ungleich hosting technologies	2	Changed publish and tags.	53	1
89	2015-06-15 16:05:44.487266+02	3	Blog	2		11	1
90	2015-06-15 17:31:20.07251+02	5	Preview of the ungleich hosting technologies	2	Changed abstract and tags.	53	1
91	2015-06-15 22:11:20.148583+02	20	magical-bern-switzerland.jpg	2	No fields changed.	41	1
92	2015-06-15 22:17:30.322259+02	6	OpenNebula + Openstack + Cloudstack = Open Cloud Day Bern	2	Changed publish and tags.	53	1
93	2015-06-15 22:19:52.426803+02	6	OpenNebula + Openstack + Cloudstack = Open Cloud Day Bern	2	Changed tags and main_image.	53	1
94	2015-06-15 22:21:31.396896+02	6	OpenNebula + Openstack + Cloudstack = Open Cloud Day Bern	2	Changed slug and tags.	53	1
95	2015-06-16 10:02:02.348565+02	1	Title Meta for Blog (blog, en-us)	1		60	1
96	2015-06-16 10:02:34.781253+02	3	Blog	2		11	1
97	2015-06-16 10:08:34.882691+02	23	380600.png	3		41	1
98	2015-06-16 10:09:21.40288+02	1	Title Meta for Blog (blog, en-us)	2	Changed keywords.	60	1
99	2015-06-16 10:09:30.836111+02	3	Blog	2		11	1
100	2015-06-16 10:21:30.955727+02	1	Title Meta for Blog (blog, en-us)	2	Changed description.	60	1
101	2015-06-16 10:21:40.885815+02	3	Blog	2		11	1
102	2015-06-16 22:11:45.853073+02	5	conference	1		51	1
103	2015-06-16 22:13:52.403868+02	7	A great OpenCloudDay 2015 in Bern	1		53	1
104	2015-06-16 23:02:07.980118+02	7	A great OpenCloudDay 2015 in Bern	2	Changed tags.	53	1
105	2015-06-16 23:21:51.253139+02	7	A great OpenCloudDay 2015 in Bern	2	Changed tags and main_image.	53	1
106	2015-06-16 23:22:23.131324+02	7	A great OpenCloudDay 2015 in Bern	2	Changed publish and tags.	53	1
107	2015-06-21 10:25:00.377457+02	6	digitalglarus	1		51	1
108	2015-06-21 10:30:44.63475+02	8	The merger of Born Informatik and adesso Schweiz AG	1		53	1
109	2015-06-21 10:39:11.215368+02	8	The merger of Born Informatik and adesso Schweiz AG	2	Changed tags and author.	53	1
110	2015-06-22 10:04:01.598254+02	8	The merger of Born Informatik and adesso Schweiz AG	2	Changed abstract and tags.	53	1
111	2015-06-22 23:32:43.975477+02	8	The merger of Born Informatik and adesso Schweiz AG	2	Changed tags.	53	1
112	2015-06-22 23:32:53.563821+02	8	The merger of Born Informatik and adesso Schweiz AG	2	Changed tags.	53	1
113	2015-06-22 23:57:05.197117+02	8	The merger of Born Informatik and adesso Schweiz AG	2	Changed publish, tags and meta_keywords.	53	1
114	2015-06-26 11:44:24.689614+02	9	Swiss Postgres Conference with cdist	1		53	1
115	2015-07-20 21:15:15.624943+02	10	Digital Glarus: The first meetup meeting	1		53	1
116	2015-07-20 21:33:03.280347+02	10	Digital Glarus: The first meetup meeting	2	Changed publish, tags and meta_keywords.	53	1
117	2015-07-27 00:38:36.977578+02	11	Digital Glarus: Call for Hacking	1		53	1
118	2015-07-27 00:44:20.704181+02	11	Digital Glarus: Call for Hacking	2	Changed abstract and tags.	53	1
119	2015-07-27 01:55:50.68159+02	11	Digital Glarus: Call for Hacking	2	Changed publish and tags.	53	1
120	2015-09-26 21:15:48.144401+02	11	Digital Glarus: Call for Hacking	2	Changed tags.	53	1
121	2015-09-26 21:45:15.024072+02	11	Digital Glarus: Call for Hacking	2	Changed tags.	53	1
122	2015-09-26 21:47:05.14917+02	11	Digital Glarus: Call for Hacking	2	Changed tags and main_image.	53	1
123	2015-09-27 00:15:52.422601+02	11	Digital Glarus: Call for Hacking	2	Changed tags.	53	1
124	2015-09-27 00:16:06.257686+02	10	Digital Glarus: The first meetup meeting	2	Changed tags.	53	1
125	2015-09-27 00:57:33.473305+02	10	Digital Glarus: The first meetup meeting	2	Changed tags and main_image.	53	1
126	2015-09-29 17:23:12.576148+02	12	Test for Raul	1		53	1
127	2015-09-29 21:05:05.969378+02	12	Test for Raul	2	Changed publish, abstract and tags.	53	1
128	2015-09-29 21:05:41.218424+02	1	https://dynamicweb-staging.ungleich.ch/blog	2	Changed domain.	7	1
129	2015-09-29 21:05:53.560601+02	12	Test for Raul	2	Changed tags and sites.	53	1
130	2015-09-29 21:06:54.023847+02	1	dynamicweb-staging.ungleich.ch/blog	2	Changed domain.	7	1
131	2015-09-29 21:07:01.793033+02	12	Test for Raul	2	Changed tags.	53	1
132	2015-09-29 21:07:53.038053+02	1	dynamicweb-staging.ungleich.ch	2	Changed domain.	7	1
133	2015-09-30 07:39:14.7488+02	12	Test for Raul	2	Changed publish and tags.	53	1
134	2015-09-30 07:40:04.059434+02	12	Test for Raul	2	Changed publish and tags.	53	1
135	2015-09-30 07:41:38.432714+02	12	Test for Raul	2	Changed publish and tags.	53	1
136	2015-09-30 07:44:08.328661+02	3	Blog	2	Changed overwrite_url and xframe_options.	11	1
137	2015-09-30 07:44:35.49613+02	3	Blog	2	Changed xframe_options.	11	1
138	2015-09-30 07:45:11.171587+02	12	Test for Raul	2	Changed tags.	53	1
139	2015-09-30 07:56:03.792794+02	12	Test for Raul	2	Changed publish and tags.	53	1
140	2015-09-30 07:59:10.455383+02	1	UngleichPage object	2	Changed image.	56	1
141	2015-09-30 08:00:06.440817+02	12	Test for Raul	2	Changed publish and tags.	53	1
142	2015-10-04 18:27:41.515203+02	5	home	1		11	1
143	2015-10-04 18:46:32.888645+02	5	home	2	Changed overwrite_url and xframe_options.	11	1
144	2015-10-04 18:47:36.318099+02	5	digital glarus home	2		11	1
145	2015-10-04 19:28:39.173545+02	3	Blog	2	Changed template and xframe_options.	11	1
146	2015-10-04 19:28:52.048834+02	3	Blog	2		11	1
147	2015-10-04 23:22:34.002783+02	8	ffff	1		11	1
148	2015-10-04 23:22:53.679733+02	9	cccccccccccccc	1		11	1
149	2015-10-04 23:27:23.576142+02	8	fooffff	2		11	1
150	2015-10-04 23:27:56.841563+02	9	ccccccccccccc	2		11	1
151	2015-10-04 23:28:47.453119+02	5	home	2	Changed overwrite_url, soft_root and xframe_options.	11	1
152	2015-10-04 23:28:58.351021+02	5	digital glarus home	2		11	1
153	2015-10-04 23:34:26.201087+02	1	Home	2		11	1
154	2015-10-04 23:35:55.056467+02	5	home	2	Changed xframe_options.	11	1
155	2015-10-04 23:40:26.364914+02	5	home	2	Changed overwrite_url and xframe_options.	11	1
156	2015-10-05 00:49:38.179792+02	5	home	2	Changed xframe_options.	11	1
157	2015-10-05 00:50:29.926486+02	5	home	2	Changed overwrite_url and xframe_options.	11	1
158	2015-10-05 00:51:02.333548+02	1	Home	3		11	1
159	2015-10-05 00:51:13.6503+02	5	digital glarus home	2		11	1
160	2015-10-05 00:51:15.345952+02	5	digital glarus home	2		11	1
161	2015-10-05 00:51:37.480905+02	5	digital glarus home	2		11	1
162	2015-10-05 00:52:23.657329+02	3	Blog	2	Changed soft_root and xframe_options.	11	1
163	2015-10-05 00:53:00.326797+02	3	Blog	2		11	1
164	2015-10-05 00:55:16.003054+02	3	Blog	2	Changed soft_root and xframe_options.	11	1
165	2015-10-05 00:55:24.575408+02	5	home	2	Changed soft_root and xframe_options.	11	1
167	2015-10-05 00:55:37.458085+02	3	Blog	2		11	1
168	2015-10-05 00:59:50.474732+02	5	home	2	Changed soft_root and xframe_options.	11	1
169	2015-10-05 00:59:54.499159+02	5	digital glarus home	2		11	1
170	2015-10-29 19:07:02.121984+01	4	rscnt	1		4	1
171	2015-11-05 08:30:25.946184+01	3	Blog	2	Changed title, slug, menu_title, page_title and meta_description.	11	1
172	2015-11-05 08:34:37.063722+01	3	Blog	2		11	1
173	2016-02-08 10:36:34.721547+01	1	Home Gallery	1		61	1
174	2016-02-08 10:38:02.26985+01	5	digital glarus home	2		11	1
175	2016-02-08 10:38:35.956034+01	12	supporters	1		11	1
176	2016-02-08 10:39:15.215809+01	12	supporters	2	Changed overwrite_url and xframe_options.	11	1
177	2016-02-08 10:40:31.137401+01	12	supporters	2	Changed overwrite_url and xframe_options.	11	1
178	2016-02-08 10:40:46.488973+01	12	supporters	2		11	1
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 178, true);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: app
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	log entry	admin	logentry
2	permission	auth	permission
3	group	auth	group
4	user	auth	user
5	content type	contenttypes	contenttype
6	session	sessions	session
7	site	sites	site
8	user setting	cms	usersettings
9	placeholder	cms	placeholder
10	cms plugin	cms	cmsplugin
11	page	cms	page
12	Page global permission	cms	globalpagepermission
13	Page permission	cms	pagepermission
14	User (page)	cms	pageuser
15	User group (page)	cms	pageusergroup
16	title	cms	title
17	placeholder reference	cms	placeholderreference
18	static placeholder	cms	staticplaceholder
19	alias plugin model	cms	aliaspluginmodel
20	cache key	menus	cachekey
21	flash	djangocms_flash	flash
22	google map	djangocms_googlemap	googlemap
23	inherit page placeholder	djangocms_inherit	inheritpageplaceholder
24	link	djangocms_link	link
25	Snippet	djangocms_snippet	snippet
26	Snippet	djangocms_snippet	snippetptr
27	teaser	djangocms_teaser	teaser
28	filer file	cmsplugin_filer_file	filerfile
29	filer folder	cmsplugin_filer_folder	filerfolder
30	filer link plugin	cmsplugin_filer_link	filerlinkplugin
31	filer teaser	cmsplugin_filer_teaser	filerteaser
32	filer video	cmsplugin_filer_video	filervideo
33	revision	reversion	revision
34	version	reversion	version
35	text	djangocms_text_ckeditor	text
36	Folder	filer	folder
37	folder permission	filer	folderpermission
38	file	filer	file
39	clipboard	filer	clipboard
40	clipboard item	filer	clipboarditem
41	image	filer	image
42	source	easy_thumbnails	source
43	thumbnail	easy_thumbnails	thumbnail
44	thumbnail dimensions	easy_thumbnails	thumbnaildimensions
45	filer image	cmsplugin_filer_image	filerimage
46	thumbnail option	cmsplugin_filer_image	thumbnailoption
47	Tag	taggit	tag
48	Tagged Item	taggit	taggeditem
49	key map	django_select2	keymap
50	blog category Translation	djangocms_blog	blogcategorytranslation
51	blog category	djangocms_blog	blogcategory
52	blog article Translation	djangocms_blog	posttranslation
53	blog article	djangocms_blog	post
54	latest posts plugin	djangocms_blog	latestpostsplugin
55	author entries plugin	djangocms_blog	authorentriesplugin
56	ungleich page	ungleich	ungleichpage
57	rails beta user	railshosting	railsbetauser
58	message	digitalglarus	message
59	Page meta info (all languages)	djangocms_page_meta	pagemeta
60	Page meta info (language-dependent)	djangocms_page_meta	titlemeta
61	dg gallery	digitalglarus	dggallery
62	rails beta user	hosting	railsbetauser
63	supporter	digitalglarus	supporter
64	dg picture	digitalglarus	dgpicture
65	dg gallery plugin	digitalglarus	dggalleryplugin
66	dg supporters plugin	digitalglarus	dgsupportersplugin
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('django_content_type_id_seq', 66, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: app
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2015-06-12 18:47:37.586053+02
2	auth	0001_initial	2015-06-12 18:47:40.078096+02
3	admin	0001_initial	2015-06-12 18:47:40.720962+02
4	sites	0001_initial	2015-06-12 18:47:40.90432+02
5	cms	0001_initial	2015-06-12 18:47:46.81365+02
6	cms	0002_auto_20140816_1918	2015-06-12 18:47:52.040742+02
7	cms	0003_auto_20140926_2347	2015-06-12 18:47:52.324788+02
8	cms	0004_auto_20140924_1038	2015-06-12 18:48:05.488729+02
9	cms	0005_auto_20140924_1039	2015-06-12 18:48:05.781437+02
10	cms	0006_auto_20140924_1110	2015-06-12 18:48:06.81011+02
11	cms	0007_auto_20141028_1559	2015-06-12 18:48:07.423593+02
12	cms	0008_auto_20150208_2149	2015-06-12 18:48:07.901227+02
13	cms	0008_auto_20150121_0059	2015-06-12 18:48:08.605592+02
14	cms	0009_merge	2015-06-12 18:48:08.904628+02
15	cms	0010_migrate_use_structure	2015-06-12 18:48:09.357941+02
16	cms	0011_auto_20150419_1006	2015-06-12 18:48:09.966304+02
17	filer	0001_initial	2015-06-12 18:48:13.197141+02
18	cmsplugin_filer_file	0001_initial	2015-06-12 18:48:13.937341+02
19	cmsplugin_filer_folder	0001_initial	2015-06-12 18:48:14.60625+02
20	cmsplugin_filer_image	0001_initial	2015-06-12 18:48:16.090267+02
21	cmsplugin_filer_link	0001_initial	2015-06-12 18:48:16.873574+02
22	cmsplugin_filer_link	0002_auto_20150612_1635	2015-06-12 18:48:17.230453+02
23	cmsplugin_filer_teaser	0001_initial	2015-06-12 18:48:18.132015+02
24	cmsplugin_filer_video	0001_initial	2015-06-12 18:48:19.031049+02
25	digitalglarus	0001_initial	2015-06-12 18:48:19.432218+02
26	digitalglarus	0002_auto_20150527_1023	2015-06-12 18:48:19.906423+02
27	digitalglarus	0002_auto_20150522_0450	2015-06-12 18:48:20.007307+02
28	digitalglarus	0003_merge	2015-06-12 18:48:20.073792+02
29	taggit	0001_initial	2015-06-12 18:48:21.308116+02
30	djangocms_blog	0001_initial	2015-06-12 18:48:27.326915+02
31	djangocms_blog	0002_post_sites	2015-06-12 18:48:28.662507+02
32	djangocms_blog	0003_auto_20141201_2252	2015-06-12 18:48:29.295249+02
33	djangocms_blog	0004_auto_20150108_1435	2015-06-12 18:48:30.336189+02
34	djangocms_blog	0005_auto_20150212_1118	2015-06-12 18:48:31.145054+02
35	djangocms_blog	0006_auto_20150612_1635	2015-06-12 18:48:32.195251+02
36	djangocms_flash	0001_initial	2015-06-12 18:48:32.512199+02
37	djangocms_googlemap	0001_initial	2015-06-12 18:48:32.862443+02
38	djangocms_inherit	0001_initial	2015-06-12 18:48:33.378062+02
39	djangocms_link	0001_initial	2015-06-12 18:48:34.295429+02
40	djangocms_link	0002_auto_20140929_1705	2015-06-12 18:48:34.469398+02
41	djangocms_link	0003_auto_20150212_1310	2015-06-12 18:48:34.657091+02
42	djangocms_snippet	0001_initial	2015-06-12 18:48:36.072264+02
43	djangocms_teaser	0001_initial	2015-06-12 18:48:36.698633+02
44	djangocms_text_ckeditor	0001_initial	2015-06-12 18:48:37.165737+02
45	easy_thumbnails	0001_initial	2015-06-12 18:48:39.062327+02
46	easy_thumbnails	0002_thumbnaildimensions	2015-06-12 18:48:39.408439+02
47	filer	0002_auto_20150612_1635	2015-06-12 18:48:39.767056+02
48	reversion	0001_initial	2015-06-12 18:48:41.231149+02
49	reversion	0002_auto_20141216_1509	2015-06-12 18:48:42.220029+02
50	sessions	0001_initial	2015-06-12 18:48:42.787999+02
51	ungleich	0001_initial	2015-06-12 18:48:43.91062+02
52	ungleich	0002_ungleichpage_image	2015-06-12 18:48:44.696539+02
53	ungleich	0003_remove_ungleichpage_image_header	2015-06-12 18:48:45.323423+02
54	djangocms_page_meta	0001_initial	2015-06-16 09:51:34.515936+02
55	djangocms_blog	0007_auto_20150616_0751	2015-06-16 09:52:05.543796+02
56	djangocms_page_meta	0002_auto_20150616_0751	2015-06-16 09:52:07.373163+02
57	cms	0012_auto_20150607_2207	2016-02-08 10:35:03.533701+01
58	cmsplugin_filer_link	0002_auto_20150610_1616	2016-02-08 10:35:03.802964+01
59	digitalglarus	0004_supporter	2016-02-08 10:35:03.967529+01
60	digitalglarus	0005_auto_20160208_0218	2016-02-08 10:35:04.020542+01
61	digitalglarus	0006_dggallery_dggalleryplugin_dgpicture	2016-02-08 10:35:04.829124+01
62	taggit	0002_auto_20150616_2121	2016-02-08 10:35:04.93505+01
63	filer	0002_auto_20150610_1616	2016-02-08 10:35:05.096611+01
64	djangocms_blog	0006_auto_20150214_1907	2016-02-08 10:35:05.92767+01
65	djangocms_blog	0007_auto_20150719_0933	2016-02-08 10:35:08.635342+01
66	djangocms_blog	0006_auto_20150610_1616	2016-02-08 10:35:09.644894+01
67	djangocms_blog	0008_merge	2016-02-08 10:35:10.417325+01
68	djangocms_blog	0009_auto_20160208_0911	2016-02-08 10:35:11.654892+01
69	djangocms_link	0004_auto_20160208_0911	2016-02-08 10:35:11.830713+01
70	djangocms_page_meta	0002_auto_20150807_0936	2016-02-08 10:35:12.082334+01
71	djangocms_page_meta	0003_auto_20160208_0911	2016-02-08 10:35:13.21645+01
72	digitalglarus	0007_auto_20160208_1031	2016-02-14 17:03:50.1734+01
73	digitalglarus	0008_dgsupportersplugin	2016-02-14 17:03:50.930529+01
74	digitalglarus	0009_remove_dgsupportersplugin_dgsupporters	2016-02-14 17:03:51.367469+01
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('django_migrations_id_seq', 74, true);


--
-- Data for Name: django_select2_keymap; Type: TABLE DATA; Schema: public; Owner: app
--

COPY django_select2_keymap (id, key, value, accessed_on) FROM stdin;
\.


--
-- Name: django_select2_keymap_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('django_select2_keymap_id_seq', 1, false);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: app
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
irm9c6an9s9ihgoqp0cpmk147gyzi12v	NzMwNDZjOGFiMzQzYjkzNTBjNDVhZWQzYTAyMmQ2ZGRjYjlmYjA3Yjp7ImNtc19hZG1pbl9zaXRlIjoxLCJfYXV0aF91c2VyX2hhc2giOiI5OGQ5NDg2ZjVkNGFjYzI1NGJkNWU4YzljYzRhNzBjMTA1ZWMyZTJhIiwiX2F1dGhfdXNlcl9pZCI6MSwiY21zX2VkaXQiOnRydWUsImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZSwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQifQ==	2015-06-26 19:28:56.575209+02
c9hxn2v7skuwz5j6k2n9drupqiq3w9wp	MWIyYjBhMDEwNDE3OTBmZWNkZDFjOGRkZDI5ZWZlYWZiMDMxNzIyNjp7Il9hdXRoX3VzZXJfaWQiOjEsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOThkOTQ4NmY1ZDRhY2MyNTRiZDVlOGM5Y2M0YTcwYzEwNWVjMmUyYSJ9	2015-08-13 01:44:34.167791+02
2q7xrigv8riwxzmdary3kbkbmmm2vul3	YWYzMDQxZjVjMWYxOTBiYWEwMzJmNzZmY2IwNmNlMzhiOTdkNzE0ZTp7Il9hdXRoX3VzZXJfaGFzaCI6Ijk4ZDk0ODZmNWQ0YWNjMjU0YmQ1ZThjOWNjNGE3MGMxMDVlYzJlMmEiLCJfYXV0aF91c2VyX2lkIjoxLCJjbXNfdG9vbGJhcl9kaXNhYmxlZCI6ZmFsc2UsImNtc19lZGl0Ijp0cnVlLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsImZpbGVyX2xhc3RfZm9sZGVyX2lkIjoiMiJ9	2015-08-13 13:50:28.45562+02
o9yhzaa0k26xx7hvnk5w2uoq5f8r70oz	NDVlYjE1ODE2ZTM2NWY4MjU5N2QzMzY1M2FlYjk1MzI1ZjU4OTExYzp7ImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZSwiY21zX2VkaXQiOnRydWV9	2015-08-19 14:19:53.607418+02
7s4cnu4kfs2hccibkkib41qxqq330qxv	MGMxNDMzNGNmZGZlMzljMGRkMGJiOTIzZWJhMDBiOGRhM2U3MjEzMjp7ImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZSwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJjbXNfZWRpdCI6ZmFsc2UsImNtc19hZG1pbl9zaXRlIjoxLCJfYXV0aF91c2VyX2lkIjoxLCJfYXV0aF91c2VyX2hhc2giOiI5OGQ5NDg2ZjVkNGFjYzI1NGJkNWU4YzljYzRhNzBjMTA1ZWMyZTJhIiwiZmlsZXJfbGFzdF9mb2xkZXJfaWQiOiI3In0=	2015-06-28 07:02:09.521374+02
vn7n1uxj515z59h12izfoh1yngf5iyxg	MWIyYjBhMDEwNDE3OTBmZWNkZDFjOGRkZDI5ZWZlYWZiMDMxNzIyNjp7Il9hdXRoX3VzZXJfaWQiOjEsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOThkOTQ4NmY1ZDRhY2MyNTRiZDVlOGM5Y2M0YTcwYzEwNWVjMmUyYSJ9	2015-08-23 18:04:10.896781+02
u300329af7b1feo24pliih9wz4y15g3m	MmQ2ODM2ZmY2NjcyMGIzZDZhNTgwNWQ1NDlhNjkwOTNhN2NjODMzNzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiY21zX3Rvb2xiYXJfZGlzYWJsZWQiOmZhbHNlLCJfYXV0aF91c2VyX2hhc2giOiI5OGQ5NDg2ZjVkNGFjYzI1NGJkNWU4YzljYzRhNzBjMTA1ZWMyZTJhIiwiY21zX2VkaXQiOnRydWUsIl9hdXRoX3VzZXJfaWQiOjF9	2015-06-28 07:04:12.268289+02
r7prkd96h5iyrcpuc7h1ewgak5y9yqvd	MWI0NTFhYWYzMWIzY2FkZTMzMGUyZGNlNTAyMWViZjY3ZWZhYTdkNjp7ImZpbGVyX2xhc3RfZm9sZGVyX2lkIjpudWxsLCJjbXNfZWRpdCI6dHJ1ZSwiY21zX2FkbWluX3NpdGUiOjEsIl9hdXRoX3VzZXJfaWQiOjEsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiY21zX2xvZ19sYXRlc3QiOjQ3LCJjbXNfdG9vbGJhcl9kaXNhYmxlZCI6ZmFsc2UsIl9hdXRoX3VzZXJfaGFzaCI6Ijk4ZDk0ODZmNWQ0YWNjMjU0YmQ1ZThjOWNjNGE3MGMxMDVlYzJlMmEifQ==	2015-06-27 15:23:25.252719+02
stxduhogbri7f5uvsbggqxfa5durcl9d	OGQ1Yzk2ZWUzOWM2ZTUxNjYzZTgzMTAwOTMxNWRhNjljMTc4YmNiNzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiY21zX2FkbWluX3NpdGUiOjEsImNtc19lZGl0Ijp0cnVlLCJfYXV0aF91c2VyX2lkIjoxLCJmaWxlcl9sYXN0X2ZvbGRlcl9pZCI6IjIiLCJfYXV0aF91c2VyX2hhc2giOiI5OGQ5NDg2ZjVkNGFjYzI1NGJkNWU4YzljYzRhNzBjMTA1ZWMyZTJhIiwiY21zX3Rvb2xiYXJfZGlzYWJsZWQiOmZhbHNlfQ==	2015-06-30 23:22:23.649062+02
wfzzuu9ooymxe0kz8m5a7unvkf743ptx	MDFhY2NhOWVjNjE5ZDlkNDI4ZTUwYzMxMjA5NDIxMGNiMzNjMGIyNTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiY21zX2FkbWluX3NpdGUiOjEsImNtc19lZGl0Ijp0cnVlLCJfYXV0aF91c2VyX2lkIjoxLCJmaWxlcl9sYXN0X2ZvbGRlcl9pZCI6IjkiLCJfYXV0aF91c2VyX2hhc2giOiI5OGQ5NDg2ZjVkNGFjYzI1NGJkNWU4YzljYzRhNzBjMTA1ZWMyZTJhIiwiY21zX3Rvb2xiYXJfZGlzYWJsZWQiOmZhbHNlfQ==	2015-07-10 11:45:51.459851+02
p8f8hr94tp8p8h3r6jqn4e2fhyfjfdsm	MDdjM2M0N2FjZTRjMDhhNTZhMWU0ZWJiOWU5YmVjMGUyMzEyYWU5Mzp7ImNtc19lZGl0IjpmYWxzZX0=	2015-06-29 16:02:38.430264+02
65pa9lzb2pux8uen15p0nprazzhjy3jy	NDVlYjE1ODE2ZTM2NWY4MjU5N2QzMzY1M2FlYjk1MzI1ZjU4OTExYzp7ImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZSwiY21zX2VkaXQiOnRydWV9	2015-06-29 16:02:38.715406+02
kbbr9swxmy1bg3ft4513xj30de2e468m	NDVlYjE1ODE2ZTM2NWY4MjU5N2QzMzY1M2FlYjk1MzI1ZjU4OTExYzp7ImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZSwiY21zX2VkaXQiOnRydWV9	2015-06-29 16:02:38.716762+02
48e7l9i82zr7p70nclduvom343atknqu	NDVlYjE1ODE2ZTM2NWY4MjU5N2QzMzY1M2FlYjk1MzI1ZjU4OTExYzp7ImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZSwiY21zX2VkaXQiOnRydWV9	2015-06-29 16:02:38.876276+02
xlxl8q57irsexpitxdilwika0jgyexnw	MzNhYWRlZWJlZmQ5MTJkNDhjYmNkZDljODYyNTM5OTNjNDFkMDA3MDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOThkOTQ4NmY1ZDRhY2MyNTRiZDVlOGM5Y2M0YTcwYzEwNWVjMmUyYSIsIl9hdXRoX3VzZXJfaWQiOjF9	2015-07-13 15:56:24.81215+02
4bi8l75ny44r8m7wa7idfsqpk2gqjk2n	OGYwNDExNjdmNGY5MGQ4MzQ3YjQzMTM4OTFmMjg2ODkxYWVlMTNkNzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMjQxZDIzY2I3ZjAyNDYzOWJmOTkwYjI2NjY1MjIxYWQwNDg0MWM4MCIsIl9hdXRoX3VzZXJfaWQiOjN9	2015-08-01 13:31:35.598436+02
ev4qckmxp1oshcpd1k6qzlb27i450hc5	YTAwMTdiNmM1YWNhMDczZDU4OGZiNDI0YjhmYjg1MGI5MjcxZjI4ZDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiY21zX2FkbWluX3NpdGUiOjEsImNtc19lZGl0IjpmYWxzZSwiX2F1dGhfdXNlcl9pZCI6MSwiZmlsZXJfbGFzdF9mb2xkZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiOThkOTQ4NmY1ZDRhY2MyNTRiZDVlOGM5Y2M0YTcwYzEwNWVjMmUyYSIsImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZX0=	2015-06-30 10:22:30.986731+02
5rdzi2gvz72ddzta0pixtzzwd3w8yaxr	NDVlYjE1ODE2ZTM2NWY4MjU5N2QzMzY1M2FlYjk1MzI1ZjU4OTExYzp7ImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZSwiY21zX2VkaXQiOnRydWV9	2015-08-04 22:57:28.1185+02
kb7mvjoecqs7r9ujhxunhla1giik5uf6	NDVlYjE1ODE2ZTM2NWY4MjU5N2QzMzY1M2FlYjk1MzI1ZjU4OTExYzp7ImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZSwiY21zX2VkaXQiOnRydWV9	2015-08-09 21:07:37.734037+02
gmrs24368tmv3hufz986jgqbzu6px6ar	NDcxMzFiMzdhMWJhMTQ4YmY4ZTE3OWY5MTUzNzBmZjgzZTNlMTEyZjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MSwiY21zX2FkbWluX3NpdGUiOjEsImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZSwiY21zX2VkaXQiOnRydWUsIl9hdXRoX3VzZXJfaGFzaCI6IjliMTRiNDNiZWVlYmQwYWRkNmRiNWQzNmU0NjgyNjA4YWY4NTFhZjgifQ==	2015-10-18 19:23:37.187041+02
6z3a8q91jij74cyiwzqpontrn80262e6	OTQ2NTI3ZWFkZTIxYWU0Y2JmNDM0ZjMzZGFiZGVhYmJiNTE0YWM4Yjp7ImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZSwiY21zX2VkaXQiOnRydWV9	2015-10-18 19:29:17.644209+02
qv502wr47gacb6nx2lerjj0o46o1om0z	NDViOGM4ZGQ5NmJjZmRkODcyYjgyZjc4NDdiYTg0MjYzNTQxM2Q5Mzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MSwiY21zX2VkaXQiOnRydWUsImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZSwiX2F1dGhfdXNlcl9oYXNoIjoiOThkOTQ4NmY1ZDRhY2MyNTRiZDVlOGM5Y2M0YTcwYzEwNWVjMmUyYSJ9	2015-08-23 18:39:49.630917+02
htro650g97gxpzree1asgmkwpcu7x7jr	MWQyOGMzODRiNWRiYmM2MWE0ZjM2YzUyNTRmYmMyYzU4NWRkZDk5ZTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiOWIxNGI0M2JlZWViZDBhZGQ2ZGI1ZDM2ZTQ2ODI2MDhhZjg1MWFmOCIsIl9hdXRoX3VzZXJfaWQiOjF9	2015-10-13 21:08:08.974157+02
01aux1ksrbxh348inxe6h3tkku361qm6	ZGNlMzY5NTEzMjZjNDAxMDBjMThjYzQ1MDk2YmQ4YTRkYWM5NmNhMTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiY21zX2xvZ19sYXRlc3QiOjEzMywiX2F1dGhfdXNlcl9oYXNoIjoiOWIxNGI0M2JlZWViZDBhZGQ2ZGI1ZDM2ZTQ2ODI2MDhhZjg1MWFmOCIsIl9hdXRoX3VzZXJfaWQiOjF9	2015-10-14 07:39:14.825758+02
mraxuqd39i2tw2j57swnysr1qq8pe87k	NDQ2NjQ2MTczMDZjNjBkNTViMWUwYjYyZTIxZjE1OWQ0OTFiYTZkZTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiZmlsZXJfbGFzdF9mb2xkZXJfaWQiOiI1IiwiX2F1dGhfdXNlcl9pZCI6MSwiX2F1dGhfdXNlcl9oYXNoIjoiNTAyOGI3NGM1MmIxYTc1ZDAzMDViMWU2MTM1YzEyNjcyMDdlYjY4MyJ9	2015-11-23 16:34:16.978407+01
hjgzzoam38t7ytvdqpnk84zcuvcrqpy4	OWVhZmJkZjBmNjAyZmIxMjYxNTA5Y2UwMDNlMjNlYmNjY2Q0ZWViNzp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiY21zX2FkbWluX3NpdGUiOjEsImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZSwiX2F1dGhfdXNlcl9pZCI6MSwiX2F1dGhfdXNlcl9oYXNoIjoiNTAyOGI3NGM1MmIxYTc1ZDAzMDViMWU2MTM1YzEyNjcyMDdlYjY4MyIsImNtc19lZGl0Ijp0cnVlfQ==	2015-11-28 23:42:19.145952+01
87r6fn3a27l08q1keqhsynz70cdcz1d1	Y2JiMjhjY2ZjN2VkODkxMGZhM2M0N2YxOWViYWJmMjg5ZjFiYzAwZjp7ImZpbGVyX2xhc3RfZm9sZGVyX2lkIjoiMSIsImNtc19hZG1pbl9zaXRlIjoxLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjUwMjhiNzRjNTJiMWE3NWQwMzA1YjFlNjEzNWMxMjY3MjA3ZWI2ODMiLCJfYXV0aF91c2VyX2lkIjoxLCJjbXNfZWRpdCI6ZmFsc2UsImNtc190b29sYmFyX2Rpc2FibGVkIjpmYWxzZX0=	2016-02-28 17:08:54.499325+01
36rka2cgwxzrc79cmuj6ujtxkdtbj9mk	OGMxZDhkNTVhZTA4NjBjMmNmYjVkOGNlNjJkYTU5ZGYzNzBiYzVmODp7ImNtc19lZGl0IjpmYWxzZSwiX2F1dGhfdXNlcl9oYXNoIjoiOWIxNGI0M2JlZWViZDBhZGQ2ZGI1ZDM2ZTQ2ODI2MDhhZjg1MWFmOCIsImNtc19hZG1pbl9zaXRlIjoxLCJmaWxlcl9sYXN0X2ZvbGRlcl9pZCI6IjUiLCJjbXNfdG9vbGJhcl9kaXNhYmxlZCI6ZmFsc2UsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MX0=	2015-10-19 00:59:59.17452+02
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: app
--

COPY django_site (id, domain, name) FROM stdin;
1	dynamicweb-staging.ungleich.ch	blog.ungleich.ch
\.


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Data for Name: djangocms_blog_authorentriesplugin; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_authorentriesplugin (cmsplugin_ptr_id, latest_posts) FROM stdin;
\.


--
-- Data for Name: djangocms_blog_authorentriesplugin_authors; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_authorentriesplugin_authors (id, authorentriesplugin_id, user_id) FROM stdin;
\.


--
-- Name: djangocms_blog_authorentriesplugin_authors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_authorentriesplugin_authors_id_seq', 1, false);


--
-- Data for Name: djangocms_blog_blogcategory; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_blogcategory (id, date_created, date_modified, parent_id) FROM stdin;
1	2015-06-12 19:07:21.648995+02	2015-06-12 19:07:21.649044+02	\N
2	2015-06-12 19:21:50.282983+02	2015-06-12 19:21:50.283027+02	\N
3	2015-06-12 22:24:27.358927+02	2015-06-12 22:24:27.358964+02	\N
4	2015-06-14 23:22:29.212861+02	2015-06-14 23:22:29.212901+02	\N
5	2015-06-16 22:11:45.850517+02	2015-06-16 22:11:45.850556+02	\N
6	2015-06-21 10:25:00.361649+02	2015-06-21 10:25:00.361757+02	\N
\.


--
-- Name: djangocms_blog_blogcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_blogcategory_id_seq', 6, true);


--
-- Data for Name: djangocms_blog_blogcategory_translation; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_blogcategory_translation (id, language_code, name, slug, master_id) FROM stdin;
1	en-us	announcement	announcement	1
2	en-us	opennebula	opennebula	2
3	en-us	hosting	hosting	3
4	en-us	technology	technology	4
5	en-us	conference	conference	5
6	en-us	digitalglarus	digitalglarus	6
\.


--
-- Name: djangocms_blog_blogcategory_translation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_blogcategory_translation_id_seq', 6, true);


--
-- Data for Name: djangocms_blog_latestpostsplugin; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_latestpostsplugin (cmsplugin_ptr_id, latest_posts) FROM stdin;
\.


--
-- Data for Name: djangocms_blog_latestpostsplugin_categories; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_latestpostsplugin_categories (id, latestpostsplugin_id, blogcategory_id) FROM stdin;
\.


--
-- Name: djangocms_blog_latestpostsplugin_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_latestpostsplugin_categories_id_seq', 1, false);


--
-- Data for Name: djangocms_blog_latestpostsplugin_tags; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_latestpostsplugin_tags (id, latestpostsplugin_id, tag_id) FROM stdin;
\.


--
-- Name: djangocms_blog_latestpostsplugin_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_latestpostsplugin_tags_id_seq', 1, false);


--
-- Data for Name: djangocms_blog_post; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_post (id, date_created, date_modified, date_published, date_published_end, publish, enable_comments, author_id, content_id, main_image_id, main_image_full_id, main_image_thumbnail_id) FROM stdin;
3	2015-06-12 22:25:21.334309+02	2015-06-12 22:25:53.912084+02	2015-05-08 22:24:07+02	\N	f	t	1	10	\N	\N	\N
4	2015-06-13 11:29:11.424986+02	2015-06-14 06:11:11.044024+02	2015-05-12 11:28:15+02	\N	t	t	1	11	15	\N	\N
1	2015-06-12 19:10:34.563775+02	2015-06-14 06:56:32.215333+02	2015-06-12 19:06:39+02	\N	t	t	1	7	18	\N	\N
5	2015-06-14 23:19:37.805402+02	2015-06-15 17:31:20.062429+02	2015-06-14 23:13:04+02	\N	t	f	1	12	\N	\N	\N
6	2015-06-14 23:23:32.36135+02	2015-06-15 22:21:31.387582+02	2015-06-14 23:21:18+02	\N	t	f	1	13	20	\N	\N
7	2015-06-16 22:13:52.392931+02	2015-06-16 23:22:23.122968+02	2015-06-16 22:11:22+02	\N	t	f	1	14	28	\N	\N
8	2015-06-21 10:30:44.597597+02	2015-06-22 23:57:05.18626+02	2015-06-21 10:24:37+02	\N	t	f	3	15	\N	\N	\N
9	2015-06-26 11:44:24.647018+02	2015-06-26 11:44:24.647059+02	2015-06-26 11:42:43+02	\N	f	f	1	16	\N	\N	\N
11	2015-07-27 00:38:36.92184+02	2015-09-27 00:15:52.408101+02	2015-07-27 00:32:38+02	\N	t	f	1	19	34	\N	\N
10	2015-07-20 21:15:15.52741+02	2015-09-27 00:57:33.44273+02	2015-07-20 20:58:22+02	\N	t	f	1	18	34	\N	\N
12	2015-09-29 17:23:12.476912+02	2015-09-30 08:00:06.429596+02	2015-09-29 17:23:00+02	\N	f	f	1	20	\N	\N	\N
\.


--
-- Data for Name: djangocms_blog_post_categories; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_post_categories (id, post_id, blogcategory_id) FROM stdin;
67	5	3
68	5	4
71	6	2
78	7	2
79	7	5
19	3	1
20	3	3
95	8	1
96	8	5
97	8	6
98	9	5
99	9	6
51	4	1
52	4	2
53	4	3
56	1	1
114	11	1
115	11	6
117	10	6
127	12	3
\.


--
-- Name: djangocms_blog_post_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_post_categories_id_seq', 127, true);


--
-- Name: djangocms_blog_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_post_id_seq', 12, true);


--
-- Data for Name: djangocms_blog_post_sites; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_post_sites (id, post_id, site_id) FROM stdin;
2	4	1
10	12	1
\.


--
-- Name: djangocms_blog_post_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_post_sites_id_seq', 10, true);


--
-- Data for Name: djangocms_blog_post_translation; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_post_translation (id, language_code, title, slug, abstract, meta_description, meta_keywords, meta_title, post_text, master_id) FROM stdin;
3	en-us	Application Hosting	application-hosting	<p>ungleich application hosting starts closed beta!</p>\r\n		ruby on rails, hosting, ungleich, switzerland			3
4	en-us	October 20-22 2015, Meet us in Barcelona!	opennebulaconf-2015	<p class="subheading">After Berlin, Philadelphia, Hamburg, Dublin, this time it&#39;s sunny Barcelona!</p>\r\n					4
1	en-us	ungleich blog launched	ungleich-blog-launched	<p>Stay tuned for our updates...</p>\r\n					1
5	en-us	Preview of the ungleich hosting technologies	preview-ungleich-hosting-technologies	<p>Curious which technologies are behind ungleich&nbsp;hosting?</p>\r\n		hosting, opennebula, gluster, ceph, Linux, Ruby On Rails, Django, NodeJS, GlusterFS, cdist, PostgreSQL			5
6	en-us	OpenNebula + Openstack + Cloudstack = Open Cloud Day Bern	opennebula-openstack-cloudstack-opencloudday-bern	<p>ungleich presents OpenNebula workshop this Tuesday, 16th of June 2015 in Bern at the Open Cloud Day.</p>\r\n					6
7	en-us	A great OpenCloudDay 2015 in Bern	great-opencloudday-2015-bern	<p>Great talks about OpenNebula, Openstack, Cloudstack, cdist, Ceph, Digital Glarus and much more...</p>\r\n					7
8	en-us	The merger of Born Informatik and adesso Schweiz AG	merger-born-informatik-and-adesso-schweiz-ag	<p>A short report on what happened (at the BBQ)</p>\r\n		born informatik, adesso, adesso Schweiz AG, digital glarus			8
9	en-us	Swiss Postgres Conference with cdist	swiss-postgres-conference-cdist	<p>The Swiss PostgreSQL experts meeting in Rapperswil</p>\r\n		postgresql, cdist, rapperswil, digitalglarus			9
10	en-us	Digital Glarus: The first meetup meeting	digital-glarus-first-meetup-meeting	<p>Today the &quot;Makers im Zigerschlitz&quot; met the first time</p>\r\n		digital glarus, meetup, hackers, makers, zigerschlitz			10
11	en-us	Digital Glarus: Call for Hacking	digital-glarus-call-hacking	<p>Have you ever hacked a house?</p>\r\n		hacking, digital glarus, property, security, camera, co-working			11
12	en-us	Test for Raul	test-raul	<p>Abstract</p>\r\n					12
\.


--
-- Name: djangocms_blog_post_translation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_post_translation_id_seq', 12, true);


--
-- Data for Name: djangocms_flash_flash; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_flash_flash (cmsplugin_ptr_id, file, width, height) FROM stdin;
\.


--
-- Data for Name: djangocms_googlemap_googlemap; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_googlemap_googlemap (cmsplugin_ptr_id, title, address, zipcode, city, content, zoom, lat, lng, route_planer_title, route_planer, width, height, info_window, scrollwheel, double_click_zoom, draggable, keyboard_shortcuts, pan_control, zoom_control, street_view_control) FROM stdin;
\.


--
-- Data for Name: djangocms_inherit_inheritpageplaceholder; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_inherit_inheritpageplaceholder (cmsplugin_ptr_id, from_language, from_page_id) FROM stdin;
\.


--
-- Data for Name: djangocms_link_link; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_link_link (cmsplugin_ptr_id, name, url, anchor, mailto, phone, target, page_link_id) FROM stdin;
\.


--
-- Data for Name: djangocms_page_meta_pagemeta; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_page_meta_pagemeta (id, og_type, og_author_url, og_author_fbid, og_publisher, og_app_id, twitter_author, twitter_site, twitter_type, gplus_author, gplus_type, extended_object_id, image_id, og_author_id, public_extension_id) FROM stdin;
\.


--
-- Name: djangocms_page_meta_pagemeta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_page_meta_pagemeta_id_seq', 1, false);


--
-- Data for Name: djangocms_page_meta_titlemeta; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_page_meta_titlemeta (id, keywords, description, og_description, twitter_description, gplus_description, extended_object_id, image_id, public_extension_id) FROM stdin;
1	blog, ungleich, hosting, switzerland	ungleich blog				3	\N	2
2	blog, ungleich, hosting, switzerland	ungleich blog				4	\N	\N
\.


--
-- Name: djangocms_page_meta_titlemeta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_page_meta_titlemeta_id_seq', 2, true);


--
-- Data for Name: djangocms_snippet_snippet; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_snippet_snippet (id, name, html, template) FROM stdin;
\.


--
-- Name: djangocms_snippet_snippet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_snippet_snippet_id_seq', 1, false);


--
-- Data for Name: djangocms_snippet_snippetptr; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_snippet_snippetptr (cmsplugin_ptr_id, snippet_id) FROM stdin;
\.


--
-- Data for Name: djangocms_teaser_teaser; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_teaser_teaser (cmsplugin_ptr_id, title, image, url, description, page_link_id) FROM stdin;
\.


--
-- Data for Name: djangocms_text_ckeditor_text; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_text_ckeditor_text (cmsplugin_ptr_id, body) FROM stdin;
1	Copyright © ungleich GmbH 2015\n
6	<p>Finally!</p>\n\n<p>After some years that most of our work appeared in individual blogs, we are today starting the ungleich blog. For those who have been visiting our blog before and  wonder why we are announcing it today: The previous blog was just a static site, wheras this blog is based on <img title="Link - DjangoCMS blog" id="plugin_obj_8" src="/static/cms/images/plugins/link.png" alt="Link">.</p>\n\n<p>It will be a technical, maybe even social blog. So stay tuned for our updates...</p>\n
4	<h2 class="section-heading" style="font-family: 'Open Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: 700; line-height: 1.1; color: rgb(64, 64, 64); margin-top: 60px; margin-bottom: 10px; font-size: 36px;">ungleich goes to Barcelona!</h2>\n\n<p style="margin: 30px 0px; line-height: 1.5; color: rgb(64, 64, 64); font-family: Lora, 'Times New Roman', serif; font-size: 20px;">We're on the road again! After Berlin <a href="http://www.linuxtag.org/2014/en/program/talk-details/?eventid=1238" style="color: rgb(64, 64, 64); background-color: transparent;">(LinuxTag)</a>, Philadelphia <a href="https://www.usenix.org/conference/ucms14/summit-program/presentation/schottelius" style="color: rgb(64, 64, 64); background-color: transparent;">(UCMS)</a>, Hamburg, and Dublin <a href="https://websummit.net/" style="color: rgb(64, 64, 64); background-color: transparent;">(Websummit)</a>, ungleich visits another fabulous city to meet great people out there in the OpenSource community. This time, it's sunny Barcelona!</p>\n\n<p style="margin: 30px 0px; line-height: 1.5; color: rgb(64, 64, 64); font-family: Lora, 'Times New Roman', serif; font-size: 20px;">Team ungleich is proud to announce that we are sponsoring OpenNebulaConf 2015.</p>\n\n<div class="embed-responsive embed-responsive-16by9" style="height: 0px; overflow: hidden; color: rgb(64, 64, 64); font-family: Lora, 'Times New Roman', serif; font-size: 20px; line-height: 22.8571434020996px;"><iframe src="https://2015.opennebulaconf.com/" class="embed-responsive-item" style="width: 778.325012207031px; height: 437.799987792969px; border-width: 0px;"></iframe></div>\n\n<p><span class="caption text-muted" style="color: rgb(119, 119, 119); text-align: center; font-size: 14px; padding: 10px; font-style: italic; margin: 0px; display: block; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px; font-family: Lora, 'Times New Roman', serif;">Official website of OpenNebulaConf2015</span></p>\n\n<p style="margin: 30px 0px; line-height: 1.5; color: rgb(64, 64, 64); font-family: Lora, 'Times New Roman', serif; font-size: 20px;">ungleich, a passionate supporter of <a href="http://en.wikipedia.org/wiki/Free_and_open-source_software" style="color: rgb(64, 64, 64); background-color: transparent;">FOSS</a>, has been using <a href="http://opennebula.org/" style="color: rgb(64, 64, 64); background-color: transparent;">OpenNebula</a> for a while, and now became a gold sponsor of the upcoming annual OpenNebula conference.</p>\n\n<p style="margin: 30px 0px; line-height: 1.5; color: rgb(64, 64, 64); font-family: Lora, 'Times New Roman', serif; font-size: 20px;">We will be on site at the conference to meet and exchange ideas of users and supporters of OpenNebula. It is an exciting opportunity for ungleich to contribute to the FOSS community!</p>\n\n<p style="margin: 30px 0px; line-height: 1.5; color: rgb(64, 64, 64); font-family: Lora, 'Times New Roman', serif; font-size: 20px;"><a href="http://blog.ungleich.ch/opennebulaconf-2015/#" style="color: rgb(64, 64, 64); background-color: transparent;"><img alt="" src="http://blog.ungleich.ch/img/opennebulaplusungleich.png" class="img-reponsive" style="border-width: 0px; vertical-align: middle;"></a></p>\n\n<h2 class="section-heading" style="font-family: 'Open Sans', 'Helvetica Neue', Helvetica, Arial, sans-serif; font-weight: 700; line-height: 1.1; color: rgb(64, 64, 64); margin-top: 60px; margin-bottom: 10px; font-size: 36px;">Why are we loving OpenNebula?</h2>\n\n<p style="margin: 30px 0px; line-height: 1.5; color: rgb(64, 64, 64); font-family: Lora, 'Times New Roman', serif; font-size: 20px;">Compared to bigger-named peers like Openstack or cloudstack, OpenNebula is (yet) less known in the field. There are reasons why ungleich is enthusiastic about OpenNebula, and one is its beautiful simplicity! OpenNebula is lean and is made for real world problems, very well fitted to experts at team ungleich, and maybe you.(=Linux user, FOSS supporter, distressed sysadmin!) OpenNebula is easily configurable with our configuration management <a href="http://www.nico.schottelius.org/software/cdist/" style="color: rgb(64, 64, 64); background-color: transparent;">cdist</a>.</p>\n\n<p style="margin: 30px 0px; line-height: 1.5; color: rgb(64, 64, 64); font-family: Lora, 'Times New Roman', serif; font-size: 20px;"><a href="http://blog.ungleich.ch/opennebulaconf-2015/#" style="color: rgb(64, 64, 64); background-color: transparent;"><img alt="" src="http://blog.ungleich.ch/img/cdist.png" class="img-responsive" style="border-width: 0px; vertical-align: middle; display: block; height: auto;"></a><span class="caption text-muted" style="color: rgb(119, 119, 119); text-align: center; font-size: 14px; padding: 10px; font-style: italic; margin: 0px; display: block; border-bottom-right-radius: 5px; border-bottom-left-radius: 5px;">cdist, an innovative configuration management system</span></p>\n\n<p style="margin: 30px 0px; line-height: 1.5; color: rgb(64, 64, 64); font-family: Lora, 'Times New Roman', serif; font-size: 20px;">Meet us at OpenNebulaConf 2015 and learn how small to large scale hosting infrastructures are configured with the configuration management system cdist.</p>\n\n<p style="margin: 30px 0px; line-height: 1.5; color: rgb(64, 64, 64); font-family: Lora, 'Times New Roman', serif; font-size: 20px;">We are excited to connect with many of OpenSource supporters out there, hopefully to inspire others and to be inspired! And, October in Barcelona, doesn't it just sound very tempting?!</p>\n\n<p style="margin: 30px 0px; line-height: 1.5; color: rgb(64, 64, 64); font-family: Lora, 'Times New Roman', serif; font-size: 20px;">See you soon in Barcelona!</p>\n\n<p><a href="https://blog.ungleich.ch/opennebulaconf-2015/#" style="color: rgb(64, 64, 64); text-decoration: none; font-family: Lora, 'Times New Roman', serif; font-size: 20px; line-height: 22.8571434020996px;"><img alt="" src="http://blog.ungleich.ch/img/barcelona_1.jpg" class="img-responsive" style="border-width: 0px; vertical-align: middle; display: block; height: auto;"></a></p>\n\n<p style="margin: 30px 0px; line-height: 1.5; color: rgb(64, 64, 64); font-family: Lora, 'Times New Roman', serif; font-size: 20px;"> </p>\n
13	<h2 class="section-heading">ungleich goes to Barcelona!</h2>\n\n<p> </p>\n\n<p>We're on the road again! After Berlin<a href="http://www.linuxtag.org/2014/en/program/talk-details/?eventid=1238">(LinuxTag)</a>, Philadelphia<a href="https://www.usenix.org/conference/ucms14/summit-program/presentation/schottelius">(UCMS)</a>, Hamburg, and Dublin<a href="https://websummit.net/">(Websummit)</a>, ungleich visits another fabulous city to meet great people out there in the OpenSource community. This time, it's sunny Barcelona!</p>\n\n<p>Team ungleich is proud to announce that we are sponsoring <img title="Link - OpenNebulaConf 2015." alt="Link" src="/static/cms/images/plugins/link.png" id="plugin_obj_14"></p>\n\n<p>ungleich, a passionate supporter of <a href="http://en.wikipedia.org/wiki/Free_and_open-source_software">FOSS</a>, has been using <a href="http://opennebula.org/">OpenNebula</a> for a while, and now became a gold sponsor of the upcoming annual OpenNebula conference.</p>\n\n<p>We will be on site at the conference to meet and exchange ideas of users and supporters of OpenNebula. It is an exciting opportunity for ungleich to contribute to the FOSS community!</p>\n\n<p><img title="Image - opennebulaplusungleich.png" alt="Image" src="/media/filer_public_thumbnails/filer_public/e1/76/e1761ff4-371b-4e72-a9bf-05e34029603e/opennebulaplusungleich.png__800x159_q85_crop_subsampling-2_upscale.jpg" id="plugin_obj_17"></p>\n\n<h2 class="section-heading">Why are we loving OpenNebula?</h2>\n\n<p>Compared to bigger-named peers like Openstack or cloudstack, OpenNebula is (yet) less known in the field. There are reasons why ungleich is enthusiastic about OpenNebula, and one is its beautiful simplicity! OpenNebula is lean and is made for real world problems, very well fitted to experts at team ungleich, and maybe you.(=Linux user, FOSS supporter, distressed sysadmin!) OpenNebula is easily configurable with our configuration management <a href="http://www.nico.schottelius.org/software/cdist/">cdist</a>.</p>\n\n<p><img title="Image - cdist.png" alt="Image" src="/media/filer_public_thumbnails/filer_public/5f/4b/5f4b7477-6a1d-4df5-a986-4eb342993b40/cdist.png__800x159_q85_crop_subsampling-2_upscale.jpg" id="plugin_obj_18"></p>\n\n<p>Meet us at OpenNebulaConf 2015 and learn how small to large scale hosting infrastructures are configured with the configuration management system cdist.</p>\n\n<p>We are excited to connect with many of OpenSource supporters out there, hopefully to inspire others and to be inspired! And, October in Barcelona, doesn't it just sound very tempting?!</p>\n\n<p>See you soon in Barcelona!</p>\n\n<p><img title="Image - barcelona_1.jpg" alt="Image" src="/media/filer_public_thumbnails/filer_public/a2/43/a2431f05-8480-4721-9a9f-8d9216c1a1b1/barcelona_1.jpg__935x514_q85_crop_subsampling-2_upscale.jpg" id="plugin_obj_19"></p>\n
20	<p></p>
21	<p>Recently we announced our first application hosting: <img title="Link - rails-hosting.ch" alt="Link" src="/static/cms/images/plugins/link.png" id="plugin_obj_24">. As you can see on the site, we are still in an early Beta for subscriptions, however the technology stack that we use behind it, has been in use for some years already.</p>\n\n<p>As we are an Open Source company, we are also  very open about our work. Actually, a lot of the work we do for our customers can be open sourced, because many of our customers are living the Open Source Spirit, but that is a different blog post...</p>\n\n<p>While our first incarnation of hosting was completely managed by <img title="Link - cdist" alt="Link" src="/static/cms/images/plugins/link.png" id="plugin_obj_28">, we moved on to use <img title="Link - OpenNebula" alt="Link" src="/static/cms/images/plugins/link.png" id="plugin_obj_25">, so we can let people manage their virtual machines on their own and via a WebUI.</p>\n\n<p>In our second incarnation we gave <img title="Link - Ceph" alt="Link" src="/static/cms/images/plugins/link.png" id="plugin_obj_26"> a try, however the performance was not as good as we hoped. In our current hosting we are using <img title="Link - GlusterFS" alt="Link" src="/static/cms/images/plugins/link.png" id="plugin_obj_27"> for storing the High Availability VMs.</p>\n\n<p>For the frontend to our hosting we have chosen a combination of <img title="Link - Nginx" alt="Link" src="/static/cms/images/plugins/link.png" id="plugin_obj_29">, <img title="Link - uwsgi" alt="Link" src="/static/cms/images/plugins/link.png" id="plugin_obj_33">, <img title="Link - Django" alt="Link" src="/static/cms/images/plugins/link.png" id="plugin_obj_34">, <img title="Link - DjangoCMS" alt="Link" src="/static/cms/images/plugins/link.png" id="plugin_obj_32">, <img title="Link - DjangoCMS Blog" alt="Link" src="/static/cms/images/plugins/link.png" id="plugin_obj_31"> and <img title="Link - PostgreSQL" alt="Link" src="/static/cms/images/plugins/link.png" id="plugin_obj_30">. The complete stack is configured by cdist.</p>\n\n<p> </p>\n\n<p>That's a sneak preview on what we used for our new hosting - we will write more about how we glued together all components in a future entry.</p>\n\n<p> </p>\n
22	<p><img title="Image - opencloudday.png" alt="Image" src="/media/filer_public_thumbnails/filer_public/08/81/08814b25-d36c-457d-bfc5-66c0c521eec8/opencloudday.png__800x252_q85_crop_subsampling-2_upscale.jpg" id="plugin_obj_38" style="line-height: 20.7999992370605px;"></p>\n\n<p>This gigant workshop, featuring OpenNebula, Openstack and Cloudstack technologies is happening this Tuesday, 16th of June 2015 in Bern at the Open Cloud Day.</p>\n\n<p>The first time in Switzerland (and maybe world wide) for a friendly meeting of cloud provider experts.</p>\n\n<p><img title="Image - bernbanner.jpg" alt="Image" src="/media/filer_public_thumbnails/filer_public/c7/62/c7623533-dbc4-4140-9544-f9f842dd4561/bernbanner.jpg__690x389_q85_crop_subsampling-2_upscale.jpg" id="plugin_obj_40"></p>\n\n<p>Participants will learn what are the possibilities and advantages of every system and have the opportunity to discuss with the experts in the evening.</p>\n\n<p> </p>\n\n<p><img title="Image - opennebulareferene.png" alt="Image" src="/media/filer_public_thumbnails/filer_public/a7/08/a708a1ff-b7dc-49d0-8ba9-72a9a32809dd/opennebulareferene.png__800x288_q85_crop_subsampling-2_upscale.png" id="plugin_obj_39"></p>\n\n<p>Nico Schottelius, CEO of <a href="http://www.ungleich.ch/">ungleich GmbH</a> (Linux infrastructure &amp; application hosting company based in Switzerland) will give an advanced workshop on cloud management with OpenNebula for DevOps.</p>\n\n<p>Schottelius, the author of the innovative configuration management system "cdist", is a judge of the Open Source Awards in Switzerland.</p>\n\n<p>Schottelius also teaches computer science at the university of applied sciences ZHAW.</p>\n
41	<p>Wow! That was as an amazing <img alt="Link" id="plugin_obj_42" title="Link - OpenCloudDay 2015 in Bern" src="/static/cms/images/plugins/link.png">! Not only happened the friendly meeting of <span style="line-height: 16.6399993896484px;">OpenNebula, </span>Openstack and Cloudstack, but also many great discussions about architectures and technologies. We have met people using good old Sendmail to cloud providers who reported about their experiences with Ceph  (thanks a lot <img alt="Link" id="plugin_obj_43" title="Link - @Jens" src="/static/cms/images/plugins/link.png">!). The OpenNebula workshop was not only great success with a lot of good questions, but also very much fun with an interested audience.</p>\n\n<p><img alt="Image" id="plugin_obj_49" title="Image - DSC_4958 copy.jpg-small.jpg" src="/media/filer_public_thumbnails/filer_public/ae/67/ae67ea00-d3f4-4f7e-8642-72419c40e818/dsc_4958_copyjpg-small.jpg__1333x944_q85_crop_subsampling-2_upscale.jpg"></p>\n\n<p>For that reason we plan to make an <strong>OpenNebula-Hackday</strong> in <img alt="Link" id="plugin_obj_44" title="Link - Digital Glarus" src="/static/cms/images/plugins/link.png"> soon (<img alt="Link" id="plugin_obj_45" title="Link - follow us on Twitter" src="/static/cms/images/plugins/link.png"> to get to know the exact date).</p>\n\n<p><img alt="Image" id="plugin_obj_50" title="Image - DSC_4986.png-small.jpg" src="/media/filer_public_thumbnails/filer_public/e3/fc/e3fccbb8-6cc4-4995-9e41-2a7dbc285806/dsc_4986png-small.jpg__1323x963_q85_crop_subsampling-2_upscale.jpg"></p>\n\n<p>Also much appreciated was the discussion after the workshops with the speakers of the OpenNebula, Openstack and Cloudstack workshops - and again a lot of fun (not much blaming each other, but pointing out what the current status is). Thnaks also goes to the <img alt="Link" id="plugin_obj_47" title="Link - @ICCLab" src="/static/cms/images/plugins/link.png"> for presenting a lot of interesting ideas as well as helping in the preparation of the joint cloud workshop.</p>\n\n<p><img alt="Image" id="plugin_obj_51" title="Image - DSC_5055.png-small.jpg" src="/media/filer_public_thumbnails/filer_public/a7/13/a713efd4-2d1a-4a53-84e2-8c82c781158c/dsc_5055png-small.jpg__1419x741_q85_crop_subsampling-2_upscale.jpg"></p>\n\n<p>Also very good feedback came towards the new feature of cdist, the installation support. Installation support? Yes! cdist is now officially the first (and only!) configuration management system that officially can configure your computer <strong>before</strong> the operating system is even installed by using its own PreOS!</p>\n\n<p>Apart from these technical discussions the Apero in the evening was showing many great Swiss based computer scientist who are all together working in the same spirit of Open Source. Thanks a lot to Matthias Günter and <img alt="Link" id="plugin_obj_46" title="Link - /ch/open" src="/static/cms/images/plugins/link.png"> for organising this great day!</p>\n\n<p><img alt="Image" id="plugin_obj_52" title="Image - DSC_5064.jpg-small.jpg" src="/media/filer_public_thumbnails/filer_public/ab/a3/aba3ae90-e8c5-4388-8e5b-93bdfa760863/dsc_5064jpg-small.jpg__1074x805_q85_crop_subsampling-2_upscale.jpg"></p>\n
53	<p><img alt="Image" id="plugin_obj_55" title="Image - born_1.jpg" src="/media/filer_public_thumbnails/filer_public/8b/9e/8b9e200c-b883-4ee9-b08d-84d09a2019ea/born_1.jpg__1200x900_q85_crop_subsampling-2_upscale.jpg"></p>\n\n<p>So far most of the mergers I have watched were happening in companies I am not related to, so this one is more interesting and I am giving you some details of what I have experienced so far.</p>\n\n<p><span style="line-height: 1.6;">When travelling to the barbeque last Thursday afternoon together with some colleagues, I did not expect such a well organised event to happen in such a short time. And with well organised, I am not only referring to the food and drinks, but much more to what the three speakers, </span><span style="line-height: 16.6399993896484px;">André Born (ex CEO of Born Informatik), Hansjörg Süess (the new CEO) and </span>Peter Walti (Verwaltungsrat) shared with everybody. </p>\n\n<p><img alt="Image" id="plugin_obj_56" title="Image - born_2.jpg" src="/media/filer_public_thumbnails/filer_public/78/af/78afb734-2025-458d-b634-b8d049d1c5bd/born_2.jpg__1200x900_q85_crop_subsampling-2_upscale.jpg"></p>\n\n<p><span style="line-height: 1.6;">When big things like a merger happens, people are usually afraid of changes, especially of loosing their job. However it was very clear that </span>André Born is caring for his employees and it looks like everyone will keep his or her wor place, just working for a different company.</p>\n\n<p>It is also interesting to hear that adesso Schweiz AG, who bought Born Informatik, used to employ about 75 people, wheras Born Informatik used to consist of roughly 125 people - so there is a big chance that the spirit of Born will survive within adesso.</p>\n\n<p>As a company doing business with Born and now adesso, we look forward to the upcoming changes and wish everyone good new experiences!</p>\n\n<p><img alt="Image" id="plugin_obj_57" title="Image - born_3.jpg" src="/media/filer_public_thumbnails/filer_public/05/2e/052e1ffe-6805-403b-825a-2e8e69a4f506/born_3.jpg__1200x914_q85_crop_subsampling-2_upscale.jpg"></p>\n\n<p>By the way - the pictures of the barbecue were taken in <strong>Olten</strong> - a very fitting place for two companies from <strong>Bern</strong> (Born) and <strong>Zürich</strong> (adesso) to celebrate their merger. We wonder, when will we see adesso in <img alt="Link" id="plugin_obj_58" title="Link - Digital Glarus" src="/static/cms/images/plugins/link.png">?</p>\n\n<p> </p>\n
61	<p>If you have followed the story of <img alt="Link" id="plugin_obj_62" title="Link - Digital Glarus" src="/static/cms/images/plugins/link.png">, you know that we at ungleich are modernising the Canton of Glarus and making it ready for the digital age, because we believe it is a place with a great view and potential.</p>\n\n<p>Today happened the first meetup of <img alt="Link" id="plugin_obj_63" title="Link - Makers im Zigerschlitz" src="/static/cms/images/plugins/link.png"> at which many possible topics to work on were discussed.</p>\n\n<p>We discussed various ideas for long time exposure projects (including one for using a boomerang with LEDs on it!), to help each other in home automation (switching lights on when you enter your home at night) to gaming projects.</p>\n\n<p>We also discussed various projects that are more suitable for children to get in touch with technology (using for instance the Raspberry Pi).</p>\n\n<p>If you do not yet know what the advantages of Digital Glarus <span style="line-height: 16.6399993896484px;">are</span> and why we at ungleich are investing here, <img alt="Link" id="plugin_obj_64" title="Link - follow us on Twitter" src="/static/cms/images/plugins/link.png"> for updates - we will post more articles about Digital Glarus soon.</p>\n
59	<p></p>
65	<p><strong>House hacking?</strong></p>\n\n<p>Hacking a house? You may <span>already </span>have heard of this or you may have done it already - without knowing it. A webcam at the door coupled with face recognition to open the door? House hacking! Lights that go on automatically, when you enter the door or when it is dark enough? House hacking! Using your mobile phone to open the doors? Definitely house hacking! Screens that change their content depending on your mood? Well, you get the picture...</p>\n\n<p><strong>Which house to hack?</strong></p>\n\n<p>We from ungleich are currently looking for a suitable house to buy, renovate and to turn it into the first <img id="plugin_obj_66" title="Link - Co-Working Space" alt="Link" src="/static/cms/images/plugins/link.png"> in <img id="plugin_obj_67" title="Link - Digital Glarus" alt="Link" src="/static/cms/images/plugins/link.png">. We are talking to investors, banks and potential users to select the right house to start building Digital Glarus.</p>\n\n<p><strong>Where is this house?</strong></p>\n\n<p>It will be located between Ziegelbrücke and Linthat - the exact location will be revealed soon!</p>\n\n<p><strong>Why hack this house?</strong></p>\n\n<p>As you may know, the Digital Glarus project is still very young and that also means innovative and dynamic. We want to create a modern Co-Working Space made by Hackers, for Hackers. We believe in the spirit of Open Source Software,</p>\n\n<p>of Crowdfunding and creating a home for digital nomads. Thus we offer this house to anyone, who would like to hack a house.</p>\n\n<p><strong>What am I allowed to do?</strong></p>\n\n<p>We practically allow you to do anything that is improves the house and conforms to the law. In case of doubt, just ask us!</p>\n\n<p><strong>I want to participate, but don't have any money!</strong></p>\n\n<p>We all have been in this situation that we wanted to do something, but did not have the money to realise it. As we believe in building a great Co-Working Space together, <strong>we offer financial </strong><strong>support for up to 5 projects for up to 500 CHF each.</strong></p>\n\n<p>If you want to use this money, just <img id="plugin_obj_69" title="Link - fill out the form" alt="Link" src="/static/cms/images/plugins/link.png"> with your project description. We will review all projects and if suitable, take the next step with you. You will hear back from us in any case...</p>\n\n<p><strong>How to hack this house?</strong></p>\n\n<p>If you are interested in hacking the house, drop us a message via Twitter (<img id="plugin_obj_68" title="Link - @ungleich" alt="Link" src="/static/cms/images/plugins/link.png">)  or <img id="plugin_obj_70" title="Link - fill out the project form" alt="Link" src="/static/cms/images/plugins/link.png">.</p>\n
72	Copyright...
73	<p></p>
74	Copyright © ungleich GmbH 2015\n
71	<p><img id="plugin_obj_75" src="/static/cms/images/plugins/link.png" alt="Link" title="Link - testing text"></p>\n
\.


--
-- Data for Name: easy_thumbnails_source; Type: TABLE DATA; Schema: public; Owner: app
--

COPY easy_thumbnails_source (id, storage_hash, name, modified) FROM stdin;
10	f9bde26a1556cd667f742bd34ec7c55e	filer_public/13/06/13062924-6b6a-4de5-bf32-a33a26980cfb/14473379828_84376f1229_h.jpg	2015-06-16 23:08:33.057565+02
8	f9bde26a1556cd667f742bd34ec7c55e	filer_public/17/45/1745f7a8-1347-47e4-b0f0-faf938fbee47/barcelona_1.jpg	2015-06-16 23:08:33.676714+02
7	f9bde26a1556cd667f742bd34ec7c55e	filer_public/b5/d8/b5d83050-247f-4f87-9a4a-21551237c450/cdist.png	2015-06-16 23:08:34.082247+02
9	f9bde26a1556cd667f742bd34ec7c55e	filer_public/af/1e/af1e9725-cee8-4a7e-834f-7d0f1d580c91/opennebulaplusungleich.png	2015-06-16 23:08:34.345178+02
15	f9bde26a1556cd667f742bd34ec7c55e	filer_public/fb/0e/fb0e2764-f19f-44f8-9ff7-1e4e9b84d440/14473379828_84376f1229_h.jpg	2015-06-14 05:17:43.181808+02
16	f9bde26a1556cd667f742bd34ec7c55e	filer_public/5e/36/5e36972a-9405-4b4a-9656-07b7a5b1216b/2015-06-13-220853_736x423_scrot.png	2015-06-14 06:43:08.873186+02
13	f9bde26a1556cd667f742bd34ec7c55e	filer_public/e1/76/e1761ff4-371b-4e72-a9bf-05e34029603e/opennebulaplusungleich.png	2015-06-14 06:44:02.157155+02
11	f9bde26a1556cd667f742bd34ec7c55e	filer_public/5f/4b/5f4b7477-6a1d-4df5-a986-4eb342993b40/cdist.png	2015-06-14 06:44:16.219661+02
12	f9bde26a1556cd667f742bd34ec7c55e	filer_public/a2/43/a2431f05-8480-4721-9a9f-8d9216c1a1b1/barcelona_1.jpg	2015-06-14 06:44:29.787597+02
17	f9bde26a1556cd667f742bd34ec7c55e	filer_public/14/94/14949dd7-6372-4c1f-b788-26592d278893/header-bg.jpg	2015-06-14 06:48:14.739396+02
24	f9bde26a1556cd667f742bd34ec7c55e	filer_public/ae/67/ae67ea00-d3f4-4f7e-8642-72419c40e818/dsc_4958_copyjpg-small.jpg	2015-06-16 23:16:30.897336+02
25	f9bde26a1556cd667f742bd34ec7c55e	filer_public/e3/fc/e3fccbb8-6cc4-4995-9e41-2a7dbc285806/dsc_4986png-small.jpg	2015-06-16 23:17:32.788986+02
20	f9bde26a1556cd667f742bd34ec7c55e	filer_public/bb/99/bb99bd4a-b925-492f-8b5b-3ae2984f0ab8/magical-bern-switzerland.jpg	2015-06-15 22:12:08.451327+02
19	f9bde26a1556cd667f742bd34ec7c55e	filer_public/08/81/08814b25-d36c-457d-bfc5-66c0c521eec8/opencloudday.png	2015-06-15 22:12:50.7233+02
21	f9bde26a1556cd667f742bd34ec7c55e	filer_public/a7/08/a708a1ff-b7dc-49d0-8ba9-72a9a32809dd/opennebulareferene.png	2015-06-15 22:13:15.88796+02
26	f9bde26a1556cd667f742bd34ec7c55e	filer_public/a7/13/a713efd4-2d1a-4a53-84e2-8c82c781158c/dsc_5055png-small.jpg	2015-06-16 23:18:24.302032+02
22	f9bde26a1556cd667f742bd34ec7c55e	filer_public/c7/62/c7623533-dbc4-4140-9544-f9f842dd4561/bernbanner.jpg	2015-06-15 22:24:12.559653+02
18	f9bde26a1556cd667f742bd34ec7c55e	filer_public/aa/9b/aa9b54c0-30c7-4efe-9fb0-a38ee2581796/16494988669_f4c6d00da4_b.jpg	2015-06-16 23:06:55.484897+02
27	f9bde26a1556cd667f742bd34ec7c55e	filer_public/ab/a3/aba3ae90-e8c5-4388-8e5b-93bdfa760863/dsc_5064jpg-small.jpg	2015-06-16 23:19:41.524273+02
28	f9bde26a1556cd667f742bd34ec7c55e	filer_public/db/e7/dbe708ff-86b5-448f-aab1-c84fb6c6730a/dsc_4967-small2.jpg	2015-06-16 23:21:05.259349+02
29	f9bde26a1556cd667f742bd34ec7c55e	filer_public/8b/9e/8b9e200c-b883-4ee9-b08d-84d09a2019ea/born_1.jpg	2015-06-22 21:51:39.830479+02
30	f9bde26a1556cd667f742bd34ec7c55e	filer_public/78/af/78afb734-2025-458d-b634-b8d049d1c5bd/born_2.jpg	2015-06-22 23:20:52.87245+02
31	f9bde26a1556cd667f742bd34ec7c55e	filer_public/05/2e/052e1ffe-6805-403b-825a-2e8e69a4f506/born_3.jpg	2015-06-22 23:28:28.785194+02
32	f9bde26a1556cd667f742bd34ec7c55e	filer_public/0e/5a/0e5a91f6-7a7f-4bd3-914b-6fe45cb1c0f7/glarus-meetup.jpg	2015-07-20 21:14:59.90436+02
33	f9bde26a1556cd667f742bd34ec7c55e	filer_public/64/9a/649a64f6-353c-46b0-a086-8b8c12a59a76/rackfromtop.jpg	2015-07-27 00:38:02.774687+02
34	f9bde26a1556cd667f742bd34ec7c55e	filer_public/f1/5a/f15ad75f-b780-49d0-9b88-ae2cb5e1fcbd/header-bg.jpg	2015-09-26 21:47:07.688275+02
35	f9bde26a1556cd667f742bd34ec7c55e	filer_public/5b/2e/5b2e15af-2bb6-4d69-9730-d8dd04168dea/header-bg.jpg	2015-10-29 19:12:13.273836+01
36	f9bde26a1556cd667f742bd34ec7c55e	filer_public/59/1f/591f22ae-9ed9-45e9-8cc9-8e3948b6e541/photo-1418479631014-8cbf89db3431.jpeg	2016-02-08 10:07:45.509278+01
37	f9bde26a1556cd667f742bd34ec7c55e	filer_public/6f/71/6f7166a4-b6ba-4c74-9d9d-4408f755938f/photo-1413834932717-29e7d4714192.jpeg	2016-02-08 10:07:47.375231+01
38	f9bde26a1556cd667f742bd34ec7c55e	filer_public/89/40/89409b2c-b855-4940-bb25-343da340250b/pier-on-a-beautiful-swiss-lake-hd-wallpaper-338658.jpg	2016-02-08 10:07:50.740025+01
\.


--
-- Name: easy_thumbnails_source_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('easy_thumbnails_source_id_seq', 38, true);


--
-- Data for Name: easy_thumbnails_thumbnail; Type: TABLE DATA; Schema: public; Owner: app
--

COPY easy_thumbnails_thumbnail (id, storage_hash, name, modified, source_id) FROM stdin;
1	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5f/4b/5f4b7477-6a1d-4df5-a986-4eb342993b40/cdist.png__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:10:43.961325+02	11
2	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5f/4b/5f4b7477-6a1d-4df5-a986-4eb342993b40/cdist.png__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:10:44.023362+02	11
3	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5f/4b/5f4b7477-6a1d-4df5-a986-4eb342993b40/cdist.png__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:10:44.079781+02	11
4	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5f/4b/5f4b7477-6a1d-4df5-a986-4eb342993b40/cdist.png__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:10:44.139663+02	11
5	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a2/43/a2431f05-8480-4721-9a9f-8d9216c1a1b1/barcelona_1.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:10:46.152985+02	12
6	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a2/43/a2431f05-8480-4721-9a9f-8d9216c1a1b1/barcelona_1.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:10:46.220742+02	12
7	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a2/43/a2431f05-8480-4721-9a9f-8d9216c1a1b1/barcelona_1.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:10:46.288801+02	12
8	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a2/43/a2431f05-8480-4721-9a9f-8d9216c1a1b1/barcelona_1.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:10:46.353659+02	12
9	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/e1/76/e1761ff4-371b-4e72-a9bf-05e34029603e/opennebulaplusungleich.png__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:10:46.561718+02	13
10	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/e1/76/e1761ff4-371b-4e72-a9bf-05e34029603e/opennebulaplusungleich.png__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:10:46.612733+02	13
11	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/e1/76/e1761ff4-371b-4e72-a9bf-05e34029603e/opennebulaplusungleich.png__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:10:46.670574+02	13
12	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/e1/76/e1761ff4-371b-4e72-a9bf-05e34029603e/opennebulaplusungleich.png__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:10:46.719497+02	13
17	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/fb/0e/fb0e2764-f19f-44f8-9ff7-1e4e9b84d440/14473379828_84376f1229_h.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:17:43.27573+02	15
18	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/fb/0e/fb0e2764-f19f-44f8-9ff7-1e4e9b84d440/14473379828_84376f1229_h.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:17:43.393008+02	15
19	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/fb/0e/fb0e2764-f19f-44f8-9ff7-1e4e9b84d440/14473379828_84376f1229_h.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:17:43.508375+02	15
20	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/fb/0e/fb0e2764-f19f-44f8-9ff7-1e4e9b84d440/14473379828_84376f1229_h.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-14 05:17:43.623966+02	15
21	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5e/36/5e36972a-9405-4b4a-9656-07b7a5b1216b/2015-06-13-220853_736x423_scrot.png__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:43:01.171023+02	16
22	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5e/36/5e36972a-9405-4b4a-9656-07b7a5b1216b/2015-06-13-220853_736x423_scrot.png__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:43:01.31511+02	16
23	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5e/36/5e36972a-9405-4b4a-9656-07b7a5b1216b/2015-06-13-220853_736x423_scrot.png__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:43:01.49873+02	16
24	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5e/36/5e36972a-9405-4b4a-9656-07b7a5b1216b/2015-06-13-220853_736x423_scrot.png__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:43:01.6384+02	16
25	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5e/36/5e36972a-9405-4b4a-9656-07b7a5b1216b/2015-06-13-220853_736x423_scrot.png__736x423_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:43:09.044936+02	16
26	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/e1/76/e1761ff4-371b-4e72-a9bf-05e34029603e/opennebulaplusungleich.png__800x159_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:44:02.317213+02	13
27	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5f/4b/5f4b7477-6a1d-4df5-a986-4eb342993b40/cdist.png__800x159_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:44:16.300511+02	11
28	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a2/43/a2431f05-8480-4721-9a9f-8d9216c1a1b1/barcelona_1.jpg__935x514_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:44:29.86618+02	12
29	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/14/94/14949dd7-6372-4c1f-b788-26592d278893/header-bg.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:48:14.835315+02	17
30	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/14/94/14949dd7-6372-4c1f-b788-26592d278893/header-bg.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:48:15.066752+02	17
31	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/14/94/14949dd7-6372-4c1f-b788-26592d278893/header-bg.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:48:15.303436+02	17
32	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/14/94/14949dd7-6372-4c1f-b788-26592d278893/header-bg.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:48:15.49941+02	17
33	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/aa/9b/aa9b54c0-30c7-4efe-9fb0-a38ee2581796/16494988669_f4c6d00da4_b.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:55:52.356094+02	18
34	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/aa/9b/aa9b54c0-30c7-4efe-9fb0-a38ee2581796/16494988669_f4c6d00da4_b.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:55:52.425013+02	18
35	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/aa/9b/aa9b54c0-30c7-4efe-9fb0-a38ee2581796/16494988669_f4c6d00da4_b.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:55:52.488416+02	18
36	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/aa/9b/aa9b54c0-30c7-4efe-9fb0-a38ee2581796/16494988669_f4c6d00da4_b.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-14 06:55:52.556872+02	18
37	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/08/81/08814b25-d36c-457d-bfc5-66c0c521eec8/opencloudday.png__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-14 23:25:46.25435+02	19
38	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/08/81/08814b25-d36c-457d-bfc5-66c0c521eec8/opencloudday.png__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-14 23:25:46.309709+02	19
39	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/08/81/08814b25-d36c-457d-bfc5-66c0c521eec8/opencloudday.png__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-14 23:25:46.358701+02	19
40	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/08/81/08814b25-d36c-457d-bfc5-66c0c521eec8/opencloudday.png__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-14 23:25:46.408904+02	19
41	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/bb/99/bb99bd4a-b925-492f-8b5b-3ae2984f0ab8/magical-bern-switzerland.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-14 23:27:15.654185+02	20
42	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/bb/99/bb99bd4a-b925-492f-8b5b-3ae2984f0ab8/magical-bern-switzerland.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-14 23:27:15.720538+02	20
43	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/bb/99/bb99bd4a-b925-492f-8b5b-3ae2984f0ab8/magical-bern-switzerland.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-14 23:27:15.782946+02	20
44	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/bb/99/bb99bd4a-b925-492f-8b5b-3ae2984f0ab8/magical-bern-switzerland.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-14 23:27:15.850812+02	20
45	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a7/08/a708a1ff-b7dc-49d0-8ba9-72a9a32809dd/opennebulareferene.png__64x64_q85_crop_subsampling-2_upscale.png	2015-06-14 23:27:31.292214+02	21
46	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a7/08/a708a1ff-b7dc-49d0-8ba9-72a9a32809dd/opennebulareferene.png__48x48_q85_crop_subsampling-2_upscale.png	2015-06-14 23:27:31.354218+02	21
47	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a7/08/a708a1ff-b7dc-49d0-8ba9-72a9a32809dd/opennebulareferene.png__16x16_q85_crop_subsampling-2_upscale.png	2015-06-14 23:27:31.411128+02	21
48	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a7/08/a708a1ff-b7dc-49d0-8ba9-72a9a32809dd/opennebulareferene.png__32x32_q85_crop_subsampling-2_upscale.png	2015-06-14 23:27:31.470584+02	21
49	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/08/81/08814b25-d36c-457d-bfc5-66c0c521eec8/opencloudday.png__210x10000_q85_subsampling-2.jpg	2015-06-14 23:28:13.298951+02	19
50	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/bb/99/bb99bd4a-b925-492f-8b5b-3ae2984f0ab8/magical-bern-switzerland.jpg__210x10000_q85_subsampling-2.jpg	2015-06-15 22:11:09.388276+02	20
51	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/bb/99/bb99bd4a-b925-492f-8b5b-3ae2984f0ab8/magical-bern-switzerland.jpg__960x641_q85_crop_subsampling-2_upscale.jpg	2015-06-15 22:12:08.590677+02	20
52	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/08/81/08814b25-d36c-457d-bfc5-66c0c521eec8/opencloudday.png__800x252_q85_crop_subsampling-2_upscale.jpg	2015-06-15 22:12:50.767564+02	19
53	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a7/08/a708a1ff-b7dc-49d0-8ba9-72a9a32809dd/opennebulareferene.png__210x10000_q85_subsampling-2.png	2015-06-15 22:13:05.526767+02	21
54	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a7/08/a708a1ff-b7dc-49d0-8ba9-72a9a32809dd/opennebulareferene.png__800x288_q85_crop_subsampling-2_upscale.png	2015-06-15 22:13:15.930445+02	21
55	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/c7/62/c7623533-dbc4-4140-9544-f9f842dd4561/bernbanner.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-15 22:24:05.357088+02	22
56	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/c7/62/c7623533-dbc4-4140-9544-f9f842dd4561/bernbanner.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-15 22:24:05.415309+02	22
57	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/c7/62/c7623533-dbc4-4140-9544-f9f842dd4561/bernbanner.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-15 22:24:05.472846+02	22
58	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/c7/62/c7623533-dbc4-4140-9544-f9f842dd4561/bernbanner.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-15 22:24:05.531672+02	22
59	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/c7/62/c7623533-dbc4-4140-9544-f9f842dd4561/bernbanner.jpg__690x389_q85_crop_subsampling-2_upscale.jpg	2015-06-15 22:24:12.607442+02	22
64	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/aa/9b/aa9b54c0-30c7-4efe-9fb0-a38ee2581796/16494988669_f4c6d00da4_b.jpg__210x10000_q85_subsampling-2.jpg	2015-06-16 23:06:55.601461+02	18
65	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/13/06/13062924-6b6a-4de5-bf32-a33a26980cfb/14473379828_84376f1229_h.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:33.111065+02	10
66	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/13/06/13062924-6b6a-4de5-bf32-a33a26980cfb/14473379828_84376f1229_h.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:33.2118+02	10
67	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/13/06/13062924-6b6a-4de5-bf32-a33a26980cfb/14473379828_84376f1229_h.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:33.319165+02	10
68	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/13/06/13062924-6b6a-4de5-bf32-a33a26980cfb/14473379828_84376f1229_h.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:33.573659+02	10
69	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/17/45/1745f7a8-1347-47e4-b0f0-faf938fbee47/barcelona_1.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:33.728271+02	8
70	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/17/45/1745f7a8-1347-47e4-b0f0-faf938fbee47/barcelona_1.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:33.789503+02	8
71	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/17/45/1745f7a8-1347-47e4-b0f0-faf938fbee47/barcelona_1.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:33.848783+02	8
72	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/17/45/1745f7a8-1347-47e4-b0f0-faf938fbee47/barcelona_1.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:33.990015+02	8
73	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/b5/d8/b5d83050-247f-4f87-9a4a-21551237c450/cdist.png__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:34.125277+02	7
74	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/b5/d8/b5d83050-247f-4f87-9a4a-21551237c450/cdist.png__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:34.17716+02	7
75	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/b5/d8/b5d83050-247f-4f87-9a4a-21551237c450/cdist.png__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:34.228274+02	7
76	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/b5/d8/b5d83050-247f-4f87-9a4a-21551237c450/cdist.png__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:34.283648+02	7
77	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/af/1e/af1e9725-cee8-4a7e-834f-7d0f1d580c91/opennebulaplusungleich.png__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:34.389678+02	9
78	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/af/1e/af1e9725-cee8-4a7e-834f-7d0f1d580c91/opennebulaplusungleich.png__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:34.438894+02	9
79	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/af/1e/af1e9725-cee8-4a7e-834f-7d0f1d580c91/opennebulaplusungleich.png__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:34.493014+02	9
80	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/af/1e/af1e9725-cee8-4a7e-834f-7d0f1d580c91/opennebulaplusungleich.png__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:08:34.606158+02	9
81	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/ae/67/ae67ea00-d3f4-4f7e-8642-72419c40e818/dsc_4958_copyjpg-small.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:16:23.042746+02	24
82	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/ae/67/ae67ea00-d3f4-4f7e-8642-72419c40e818/dsc_4958_copyjpg-small.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:16:23.150794+02	24
83	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/ae/67/ae67ea00-d3f4-4f7e-8642-72419c40e818/dsc_4958_copyjpg-small.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:16:23.296046+02	24
84	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/ae/67/ae67ea00-d3f4-4f7e-8642-72419c40e818/dsc_4958_copyjpg-small.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:16:23.390157+02	24
85	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/ae/67/ae67ea00-d3f4-4f7e-8642-72419c40e818/dsc_4958_copyjpg-small.jpg__1333x944_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:16:30.989038+02	24
86	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/e3/fc/e3fccbb8-6cc4-4995-9e41-2a7dbc285806/dsc_4986png-small.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:17:26.757978+02	25
87	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/e3/fc/e3fccbb8-6cc4-4995-9e41-2a7dbc285806/dsc_4986png-small.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:17:26.83992+02	25
88	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/e3/fc/e3fccbb8-6cc4-4995-9e41-2a7dbc285806/dsc_4986png-small.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:17:26.96659+02	25
89	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/e3/fc/e3fccbb8-6cc4-4995-9e41-2a7dbc285806/dsc_4986png-small.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:17:27.082646+02	25
90	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/e3/fc/e3fccbb8-6cc4-4995-9e41-2a7dbc285806/dsc_4986png-small.jpg__1323x963_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:17:32.833987+02	25
91	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a7/13/a713efd4-2d1a-4a53-84e2-8c82c781158c/dsc_5055png-small.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:18:17.443333+02	26
92	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a7/13/a713efd4-2d1a-4a53-84e2-8c82c781158c/dsc_5055png-small.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:18:17.52545+02	26
93	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a7/13/a713efd4-2d1a-4a53-84e2-8c82c781158c/dsc_5055png-small.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:18:17.610127+02	26
94	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a7/13/a713efd4-2d1a-4a53-84e2-8c82c781158c/dsc_5055png-small.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:18:17.69473+02	26
95	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/a7/13/a713efd4-2d1a-4a53-84e2-8c82c781158c/dsc_5055png-small.jpg__1419x741_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:18:24.347333+02	26
96	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/ab/a3/aba3ae90-e8c5-4388-8e5b-93bdfa760863/dsc_5064jpg-small.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:19:06.540844+02	27
97	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/ab/a3/aba3ae90-e8c5-4388-8e5b-93bdfa760863/dsc_5064jpg-small.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:19:06.627898+02	27
98	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/ab/a3/aba3ae90-e8c5-4388-8e5b-93bdfa760863/dsc_5064jpg-small.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:19:06.715347+02	27
99	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/ab/a3/aba3ae90-e8c5-4388-8e5b-93bdfa760863/dsc_5064jpg-small.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:19:06.809056+02	27
100	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/ab/a3/aba3ae90-e8c5-4388-8e5b-93bdfa760863/dsc_5064jpg-small.jpg__1074x805_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:19:41.605519+02	27
101	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/db/e7/dbe708ff-86b5-448f-aab1-c84fb6c6730a/dsc_4967-small2.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:21:05.30086+02	28
102	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/db/e7/dbe708ff-86b5-448f-aab1-c84fb6c6730a/dsc_4967-small2.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:21:05.402203+02	28
103	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/db/e7/dbe708ff-86b5-448f-aab1-c84fb6c6730a/dsc_4967-small2.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:21:05.504426+02	28
104	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/db/e7/dbe708ff-86b5-448f-aab1-c84fb6c6730a/dsc_4967-small2.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-16 23:21:05.609315+02	28
105	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/8b/9e/8b9e200c-b883-4ee9-b08d-84d09a2019ea/born_1.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-22 15:54:34.873265+02	29
106	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/8b/9e/8b9e200c-b883-4ee9-b08d-84d09a2019ea/born_1.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-22 15:54:35.035657+02	29
107	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/8b/9e/8b9e200c-b883-4ee9-b08d-84d09a2019ea/born_1.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-22 15:54:35.183649+02	29
108	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/8b/9e/8b9e200c-b883-4ee9-b08d-84d09a2019ea/born_1.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-22 15:54:35.291145+02	29
109	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/78/af/78afb734-2025-458d-b634-b8d049d1c5bd/born_2.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-22 15:54:55.716104+02	30
110	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/78/af/78afb734-2025-458d-b634-b8d049d1c5bd/born_2.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-22 15:54:55.830007+02	30
111	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/78/af/78afb734-2025-458d-b634-b8d049d1c5bd/born_2.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-22 15:54:55.95397+02	30
112	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/78/af/78afb734-2025-458d-b634-b8d049d1c5bd/born_2.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-22 15:54:56.065427+02	30
113	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/05/2e/052e1ffe-6805-403b-825a-2e8e69a4f506/born_3.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-06-22 15:55:53.935068+02	31
114	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/05/2e/052e1ffe-6805-403b-825a-2e8e69a4f506/born_3.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-06-22 15:55:54.067736+02	31
115	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/05/2e/052e1ffe-6805-403b-825a-2e8e69a4f506/born_3.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-06-22 15:55:54.190421+02	31
116	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/05/2e/052e1ffe-6805-403b-825a-2e8e69a4f506/born_3.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-06-22 15:55:54.311992+02	31
117	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/8b/9e/8b9e200c-b883-4ee9-b08d-84d09a2019ea/born_1.jpg__1200x900_q85_crop_subsampling-2_upscale.jpg	2015-06-22 21:51:39.946491+02	29
118	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/78/af/78afb734-2025-458d-b634-b8d049d1c5bd/born_2.jpg__1200x900_q85_crop_subsampling-2_upscale.jpg	2015-06-22 23:20:52.922031+02	30
119	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/05/2e/052e1ffe-6805-403b-825a-2e8e69a4f506/born_3.jpg__1200x914_q85_crop_subsampling-2_upscale.jpg	2015-06-22 23:28:28.832968+02	31
120	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/0e/5a/0e5a91f6-7a7f-4bd3-914b-6fe45cb1c0f7/glarus-meetup.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-07-20 21:15:00.018825+02	32
121	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/0e/5a/0e5a91f6-7a7f-4bd3-914b-6fe45cb1c0f7/glarus-meetup.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-07-20 21:15:00.152683+02	32
122	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/0e/5a/0e5a91f6-7a7f-4bd3-914b-6fe45cb1c0f7/glarus-meetup.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-07-20 21:15:00.251685+02	32
123	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/0e/5a/0e5a91f6-7a7f-4bd3-914b-6fe45cb1c0f7/glarus-meetup.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-07-20 21:15:00.333203+02	32
124	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/64/9a/649a64f6-353c-46b0-a086-8b8c12a59a76/rackfromtop.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-07-27 00:38:02.818644+02	33
125	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/64/9a/649a64f6-353c-46b0-a086-8b8c12a59a76/rackfromtop.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-07-27 00:38:03.03443+02	33
126	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/64/9a/649a64f6-353c-46b0-a086-8b8c12a59a76/rackfromtop.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-07-27 00:38:03.355143+02	33
127	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/64/9a/649a64f6-353c-46b0-a086-8b8c12a59a76/rackfromtop.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-07-27 00:38:03.580138+02	33
128	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/f1/5a/f15ad75f-b780-49d0-9b88-ae2cb5e1fcbd/header-bg.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-09-26 21:46:57.858365+02	34
129	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/f1/5a/f15ad75f-b780-49d0-9b88-ae2cb5e1fcbd/header-bg.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-09-26 21:46:57.978613+02	34
130	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/f1/5a/f15ad75f-b780-49d0-9b88-ae2cb5e1fcbd/header-bg.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-09-26 21:46:58.079137+02	34
131	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/f1/5a/f15ad75f-b780-49d0-9b88-ae2cb5e1fcbd/header-bg.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-09-26 21:46:58.164172+02	34
132	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/f1/5a/f15ad75f-b780-49d0-9b88-ae2cb5e1fcbd/header-bg.jpg__640x120_q85_crop_subsampling-2.jpg	2015-09-26 21:47:07.812318+02	34
133	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5b/2e/5b2e15af-2bb6-4d69-9730-d8dd04168dea/header-bg.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2015-09-30 07:59:04.293541+02	35
134	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5b/2e/5b2e15af-2bb6-4d69-9730-d8dd04168dea/header-bg.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2015-09-30 07:59:04.43128+02	35
135	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5b/2e/5b2e15af-2bb6-4d69-9730-d8dd04168dea/header-bg.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2015-09-30 07:59:04.52645+02	35
136	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5b/2e/5b2e15af-2bb6-4d69-9730-d8dd04168dea/header-bg.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2015-09-30 07:59:04.620487+02	35
137	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/5b/2e/5b2e15af-2bb6-4d69-9730-d8dd04168dea/header-bg.jpg__210x10000_q85_subsampling-2.jpg	2015-10-29 19:12:13.306433+01	35
138	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/59/1f/591f22ae-9ed9-45e9-8cc9-8e3948b6e541/photo-1418479631014-8cbf89db3431.jpeg__16x16_q85_crop_subsampling-2_upscale.jpg	2016-02-08 10:07:45.544698+01	36
139	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/59/1f/591f22ae-9ed9-45e9-8cc9-8e3948b6e541/photo-1418479631014-8cbf89db3431.jpeg__32x32_q85_crop_subsampling-2_upscale.jpg	2016-02-08 10:07:45.6877+01	36
140	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/59/1f/591f22ae-9ed9-45e9-8cc9-8e3948b6e541/photo-1418479631014-8cbf89db3431.jpeg__64x64_q85_crop_subsampling-2_upscale.jpg	2016-02-08 10:07:45.877295+01	36
141	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/59/1f/591f22ae-9ed9-45e9-8cc9-8e3948b6e541/photo-1418479631014-8cbf89db3431.jpeg__48x48_q85_crop_subsampling-2_upscale.jpg	2016-02-08 10:07:45.993528+01	36
142	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/6f/71/6f7166a4-b6ba-4c74-9d9d-4408f755938f/photo-1413834932717-29e7d4714192.jpeg__16x16_q85_crop_subsampling-2_upscale.jpg	2016-02-08 10:07:47.490346+01	37
143	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/6f/71/6f7166a4-b6ba-4c74-9d9d-4408f755938f/photo-1413834932717-29e7d4714192.jpeg__32x32_q85_crop_subsampling-2_upscale.jpg	2016-02-08 10:07:47.65833+01	37
144	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/6f/71/6f7166a4-b6ba-4c74-9d9d-4408f755938f/photo-1413834932717-29e7d4714192.jpeg__64x64_q85_crop_subsampling-2_upscale.jpg	2016-02-08 10:07:47.808593+01	37
145	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/6f/71/6f7166a4-b6ba-4c74-9d9d-4408f755938f/photo-1413834932717-29e7d4714192.jpeg__48x48_q85_crop_subsampling-2_upscale.jpg	2016-02-08 10:07:47.95721+01	37
146	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/89/40/89409b2c-b855-4940-bb25-343da340250b/pier-on-a-beautiful-swiss-lake-hd-wallpaper-338658.jpg__16x16_q85_crop_subsampling-2_upscale.jpg	2016-02-08 10:07:50.791085+01	38
147	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/89/40/89409b2c-b855-4940-bb25-343da340250b/pier-on-a-beautiful-swiss-lake-hd-wallpaper-338658.jpg__32x32_q85_crop_subsampling-2_upscale.jpg	2016-02-08 10:07:50.880522+01	38
148	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/89/40/89409b2c-b855-4940-bb25-343da340250b/pier-on-a-beautiful-swiss-lake-hd-wallpaper-338658.jpg__64x64_q85_crop_subsampling-2_upscale.jpg	2016-02-08 10:07:50.979611+01	38
149	f9bde26a1556cd667f742bd34ec7c55e	filer_public_thumbnails/filer_public/89/40/89409b2c-b855-4940-bb25-343da340250b/pier-on-a-beautiful-swiss-lake-hd-wallpaper-338658.jpg__48x48_q85_crop_subsampling-2_upscale.jpg	2016-02-08 10:07:51.0709+01	38
\.


--
-- Name: easy_thumbnails_thumbnail_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('easy_thumbnails_thumbnail_id_seq', 149, true);


--
-- Data for Name: easy_thumbnails_thumbnaildimensions; Type: TABLE DATA; Schema: public; Owner: app
--

COPY easy_thumbnails_thumbnaildimensions (id, thumbnail_id, width, height) FROM stdin;
\.


--
-- Name: easy_thumbnails_thumbnaildimensions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('easy_thumbnails_thumbnaildimensions_id_seq', 1, false);


--
-- Data for Name: filer_clipboard; Type: TABLE DATA; Schema: public; Owner: app
--

COPY filer_clipboard (id, user_id) FROM stdin;
1	1
\.


--
-- Name: filer_clipboard_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('filer_clipboard_id_seq', 1, true);


--
-- Data for Name: filer_clipboarditem; Type: TABLE DATA; Schema: public; Owner: app
--

COPY filer_clipboarditem (id, clipboard_id, file_id) FROM stdin;
\.


--
-- Name: filer_clipboarditem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('filer_clipboarditem_id_seq', 42, true);


--
-- Data for Name: filer_file; Type: TABLE DATA; Schema: public; Owner: app
--

COPY filer_file (id, file, _file_size, sha1, has_all_mandatory_data, original_filename, name, description, uploaded_at, modified_at, is_public, folder_id, owner_id, polymorphic_ctype_id) FROM stdin;
7	filer_public/b5/d8/b5d83050-247f-4f87-9a4a-21551237c450/cdist.png	13607	1421132c5c81f413fee6f0b4a1052ede907d36d0	f	cdist.png		\N	2015-06-14 04:53:59.732313+02	2015-06-14 04:53:59.732344+02	t	\N	1	41
8	filer_public/17/45/1745f7a8-1347-47e4-b0f0-faf938fbee47/barcelona_1.jpg	116194	8de95580b0443f51498f6752186baf1fd035e19a	f	barcelona_1.jpg		\N	2015-06-14 04:54:01.900735+02	2015-06-14 04:54:01.900768+02	t	\N	1	41
9	filer_public/af/1e/af1e9725-cee8-4a7e-834f-7d0f1d580c91/opennebulaplusungleich.png	41002	d9309921e2948a4cb1a883cf6b3221a8050f2397	f	opennebulaplusungleich.png		\N	2015-06-14 04:54:02.095606+02	2015-06-14 04:54:02.095636+02	t	\N	1	41
10	filer_public/13/06/13062924-6b6a-4de5-bf32-a33a26980cfb/14473379828_84376f1229_h.jpg	451277	d279f4d8ded8e53aba697f9fa1b24c960a3c4593	f	14473379828_84376f1229_h.jpg		\N	2015-06-14 04:54:07.40675+02	2015-06-14 04:54:07.406781+02	t	\N	1	41
11	filer_public/5f/4b/5f4b7477-6a1d-4df5-a986-4eb342993b40/cdist.png	13607	1421132c5c81f413fee6f0b4a1052ede907d36d0	f	cdist.png		\N	2015-06-14 05:10:43.757178+02	2015-06-14 05:10:54.32416+02	t	4	1	41
12	filer_public/a2/43/a2431f05-8480-4721-9a9f-8d9216c1a1b1/barcelona_1.jpg	116194	8de95580b0443f51498f6752186baf1fd035e19a	f	barcelona_1.jpg		\N	2015-06-14 05:10:45.825564+02	2015-06-14 05:10:54.397181+02	t	4	1	41
13	filer_public/e1/76/e1761ff4-371b-4e72-a9bf-05e34029603e/opennebulaplusungleich.png	41002	d9309921e2948a4cb1a883cf6b3221a8050f2397	f	opennebulaplusungleich.png		\N	2015-06-14 05:10:46.426921+02	2015-06-14 05:10:54.438285+02	t	4	1	41
15	filer_public/fb/0e/fb0e2764-f19f-44f8-9ff7-1e4e9b84d440/14473379828_84376f1229_h.jpg	150546	ae848e2019c0f2a0a9484ecb23d6a849a6c4aa3d	f	14473379828_84376f1229_h.jpg		\N	2015-06-14 05:17:42.6697+02	2015-06-14 05:17:45.053143+02	t	4	1	41
16	filer_public/5e/36/5e36972a-9405-4b4a-9656-07b7a5b1216b/2015-06-13-220853_736x423_scrot.png	448065	26845e9dd5c4b23f4fafe408ffff0f65acb0615a	f	2015-06-13-220853_736x423_scrot.png		\N	2015-06-14 06:43:00.30159+02	2015-06-14 06:43:03.513933+02	t	4	1	41
17	filer_public/14/94/14949dd7-6372-4c1f-b788-26592d278893/header-bg.jpg	194160	5fcc2aed3e17bbfc207f8ff3ccd68182fe77525d	f	header-bg.jpg		\N	2015-06-14 06:48:14.423315+02	2015-06-14 06:48:17.067798+02	t	6	1	41
18	filer_public/aa/9b/aa9b54c0-30c7-4efe-9fb0-a38ee2581796/16494988669_f4c6d00da4_b.jpg	164669	93c59e2645fdcbdd199c1da54b45cedc941f5cb0	f	16494988669_f4c6d00da4_b.jpg		\N	2015-06-14 06:55:52.099926+02	2015-06-14 06:55:53.927318+02	t	7	1	41
21	filer_public/a7/08/a708a1ff-b7dc-49d0-8ba9-72a9a32809dd/opennebulareferene.png	65786	483033ff28f1627a269b91abbce6c7a920c25e38	f	opennebulareferene.png		\N	2015-06-14 23:27:31.078751+02	2015-06-14 23:27:32.672429+02	t	3	1	41
19	filer_public/08/81/08814b25-d36c-457d-bfc5-66c0c521eec8/opencloudday.png	15947	d4580f70c49a22dce6534bb0051cfecb18e58b1f	f	opencloudday.png			2015-06-14 23:25:45.923609+02	2015-06-14 23:28:20.835789+02	t	3	1	41
20	filer_public/bb/99/bb99bd4a-b925-492f-8b5b-3ae2984f0ab8/magical-bern-switzerland.jpg	170541	1d4797ae9f8f8d485d149ac2539a062e1d7e2e37	f	magical-bern-switzerland.jpg			2015-06-14 23:27:15.461432+02	2015-06-15 22:11:52.857108+02	t	3	1	41
22	filer_public/c7/62/c7623533-dbc4-4140-9544-f9f842dd4561/bernbanner.jpg	403313	98b2361cd39c4b67df007f7185a410ca7783f6ff	f	bernbanner.jpg		\N	2015-06-15 22:24:05.161659+02	2015-06-15 22:24:07.530492+02	t	3	1	41
24	filer_public/ae/67/ae67ea00-d3f4-4f7e-8642-72419c40e818/dsc_4958_copyjpg-small.jpg	841973	733325ad687125847304a8478c62c2f13e43c11e	f	DSC_4958 copy.jpg-small.jpg		\N	2015-06-16 23:16:22.841897+02	2015-06-16 23:16:25.541953+02	t	2	1	41
25	filer_public/e3/fc/e3fccbb8-6cc4-4995-9e41-2a7dbc285806/dsc_4986png-small.jpg	168401	210ec718736ce86b5e93882c12c2e63544a7de2a	f	DSC_4986.png-small.jpg		\N	2015-06-16 23:17:26.357118+02	2015-06-16 23:17:28.473102+02	t	2	1	41
26	filer_public/a7/13/a713efd4-2d1a-4a53-84e2-8c82c781158c/dsc_5055png-small.jpg	152539	f0fe53ee8adc145d902c2437673c677eefeb99e5	f	DSC_5055.png-small.jpg		\N	2015-06-16 23:18:17.264158+02	2015-06-16 23:18:19.560696+02	t	2	1	41
27	filer_public/ab/a3/aba3ae90-e8c5-4388-8e5b-93bdfa760863/dsc_5064jpg-small.jpg	647922	9bfe441317db5db1d45a24734c9ebc641f4165d0	f	DSC_5064.jpg-small.jpg		\N	2015-06-16 23:19:06.235821+02	2015-06-16 23:19:08.193688+02	t	2	1	41
28	filer_public/db/e7/dbe708ff-86b5-448f-aab1-c84fb6c6730a/dsc_4967-small2.jpg	401587	1095bcff34d2c3ae89ca2d0b1d6b8e8a82ac526b	f	DSC_4967-small2.jpg		\N	2015-06-16 23:21:05.074717+02	2015-06-16 23:21:06.960703+02	t	2	1	41
29	filer_public/8b/9e/8b9e200c-b883-4ee9-b08d-84d09a2019ea/born_1.jpg	681091	916b30de4e4c5d375679d7e3a2b67cf59bbf2723	f	born_1.jpg		\N	2015-06-22 15:54:34.545928+02	2015-06-22 15:54:37.645561+02	t	9	1	41
30	filer_public/78/af/78afb734-2025-458d-b634-b8d049d1c5bd/born_2.jpg	632959	7ab7249eeeb6f4fdb15e9f322e1d18dca311aefb	f	born_2.jpg		\N	2015-06-22 15:54:55.525878+02	2015-06-22 15:55:30.786995+02	t	9	1	41
31	filer_public/05/2e/052e1ffe-6805-403b-825a-2e8e69a4f506/born_3.jpg	932382	73d323d3e6bed64f970eaa18146497d6df6ef385	f	born_3.jpg		\N	2015-06-22 15:55:53.724322+02	2015-06-22 15:57:15.785345+02	t	9	1	41
32	filer_public/0e/5a/0e5a91f6-7a7f-4bd3-914b-6fe45cb1c0f7/glarus-meetup.jpg	291801	ee012845d35032c91f09b606386cf53bb2bdf9e3	f	glarus-meetup.jpg		\N	2015-07-20 21:14:58.755465+02	2015-07-20 21:15:02.937024+02	t	2	1	41
33	filer_public/64/9a/649a64f6-353c-46b0-a086-8b8c12a59a76/rackfromtop.jpg	643106	b3c14eac4a44257a213f80faf9aab5901c9228d0	f	rackfromtop.jpg		\N	2015-07-27 00:38:02.08007+02	2015-07-27 00:38:04.487834+02	t	2	1	41
34	filer_public/f1/5a/f15ad75f-b780-49d0-9b88-ae2cb5e1fcbd/header-bg.jpg	194160	5fcc2aed3e17bbfc207f8ff3ccd68182fe77525d	f	header-bg.jpg		\N	2015-09-26 21:46:57.318333+02	2015-09-26 21:46:59.498186+02	t	10	1	41
35	filer_public/5b/2e/5b2e15af-2bb6-4d69-9730-d8dd04168dea/header-bg.jpg	194160	5fcc2aed3e17bbfc207f8ff3ccd68182fe77525d	f	header-bg.jpg		\N	2015-09-30 07:59:03.893755+02	2015-09-30 07:59:05.997069+02	t	5	1	41
36	filer_public/59/1f/591f22ae-9ed9-45e9-8cc9-8e3948b6e541/photo-1418479631014-8cbf89db3431.jpeg	626235	a02cb16ff5642926ae9a667d3af4bc3d644b7ba1	f	photo-1418479631014-8cbf89db3431.jpeg		\N	2016-02-08 10:07:45.149368+01	2016-02-08 10:07:55.084575+01	t	1	1	41
37	filer_public/6f/71/6f7166a4-b6ba-4c74-9d9d-4408f755938f/photo-1413834932717-29e7d4714192.jpeg	662876	01e7b38830d7d1150e83bc7a41c069e0a7b7f089	f	photo-1413834932717-29e7d4714192.jpeg		\N	2016-02-08 10:07:47.107155+01	2016-02-08 10:07:55.13551+01	t	1	1	41
38	filer_public/89/40/89409b2c-b855-4940-bb25-343da340250b/pier-on-a-beautiful-swiss-lake-hd-wallpaper-338658.jpg	554311	b23cb180d649a0cb9f4a518be17f17dc2f910587	f	pier-on-a-beautiful-swiss-lake-hd-wallpaper-338658.jpg		\N	2016-02-08 10:07:50.598835+01	2016-02-08 10:07:55.156364+01	t	1	1	41
\.


--
-- Name: filer_file_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('filer_file_id_seq', 38, true);


--
-- Data for Name: filer_folder; Type: TABLE DATA; Schema: public; Owner: app
--

COPY filer_folder (id, name, uploaded_at, created_at, modified_at, lft, rght, tree_id, level, owner_id, parent_id) FROM stdin;
4	13062015_Conf2015	2015-06-13 19:44:50.116189+02	2015-06-13 19:44:50.116239+02	2015-06-13 19:44:50.116262+02	4	5	1	3	1	3
5	ungleich_pages	2015-06-14 06:47:41.720159+02	2015-06-14 06:47:41.720207+02	2015-06-14 06:47:41.720231+02	1	4	2	0	1	\N
6	blog_page	2015-06-14 06:47:55.541517+02	2015-06-14 06:47:55.541567+02	2015-06-14 06:47:55.54159+02	2	3	2	1	1	5
7	ungleich_blog_launched	2015-06-14 06:55:41.136704+02	2015-06-14 06:55:41.136754+02	2015-06-14 06:55:41.136778+02	6	7	1	3	1	3
8	openclouddaybern2015	2015-06-16 23:21:25.670405+02	2015-06-16 23:21:25.670455+02	2015-06-16 23:21:25.670477+02	11	12	1	2	1	2
3	img	2015-06-13 19:44:24.018499+02	2015-06-13 19:44:24.018549+02	2015-06-14 05:10:32.32511+02	3	10	1	2	1	2
9	born_bbq_2015_06_18	2015-06-22 15:39:41.706736+02	2015-06-22 15:39:41.706787+02	2015-06-22 15:39:41.70681+02	8	9	1	3	1	3
2	articles	2015-06-13 19:44:13.866219+02	2015-06-13 19:44:13.866266+02	2015-06-14 04:53:32.802057+02	2	15	1	1	1	1
1	ungleich_blog	2015-06-12 23:10:27.076932+02	2015-06-12 23:10:27.076969+02	2015-06-12 23:10:27.07699+02	1	16	1	0	1	\N
10	test	2015-09-26 21:46:47.41333+02	2015-09-26 21:46:47.413363+02	2015-09-26 21:46:47.41338+02	13	14	1	2	1	2
\.


--
-- Name: filer_folder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('filer_folder_id_seq', 10, true);


--
-- Data for Name: filer_folderpermission; Type: TABLE DATA; Schema: public; Owner: app
--

COPY filer_folderpermission (id, type, everybody, can_edit, can_read, can_add_children, folder_id, group_id, user_id) FROM stdin;
\.


--
-- Name: filer_folderpermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('filer_folderpermission_id_seq', 1, false);


--
-- Data for Name: filer_image; Type: TABLE DATA; Schema: public; Owner: app
--

COPY filer_image (file_ptr_id, _height, _width, date_taken, default_alt_text, default_caption, author, must_always_publish_author_credit, must_always_publish_copyright, subject_location) FROM stdin;
7	159	800	2015-06-14 04:53:59.722929+02	\N	\N	\N	f	f	\N
8	514	935	2015-06-14 04:54:01.896409+02	\N	\N	\N	f	f	\N
9	159	800	2015-06-14 04:54:02.09203+02	\N	\N	\N	f	f	\N
10	1067	1600	2015-06-14 04:54:07.401576+02	\N	\N	\N	f	f	\N
11	159	800	2015-06-14 05:10:43.712913+02	\N	\N	\N	f	f	\N
12	514	935	2015-06-14 05:10:45.821758+02	\N	\N	\N	f	f	\N
13	159	800	2015-06-14 05:10:46.423519+02	\N	\N	\N	f	f	\N
15	1067	1600	2015-06-14 05:17:42.660506+02	\N	\N	\N	f	f	\N
16	423	736	2015-06-14 06:43:00.088274+02	\N	\N	\N	f	f	\N
17	1250	1900	2015-06-14 06:48:14.418306+02	\N	\N	\N	f	f	\N
18	683	1024	2015-06-14 06:55:52.095523+02	\N	\N	\N	f	f	\N
21	288	800	2015-06-14 23:27:31.074765+02	\N	\N	\N	f	f	\N
19	252	800	2015-06-14 23:25:45.91285+02				f	f	
20	641	960	2015-06-14 23:27:15.456539+02				f	f	
22	389	690	2015-06-15 22:24:05.15334+02	\N	\N	\N	f	f	\N
24	944	1333	2015-06-16 23:16:22.831995+02	\N	\N	\N	f	f	\N
25	963	1323	2015-06-16 23:17:26.352781+02	\N	\N	\N	f	f	\N
26	741	1419	2015-06-16 23:18:17.259021+02	\N	\N	\N	f	f	\N
27	805	1074	2015-06-16 23:19:06.228144+02	\N	\N	\N	f	f	\N
28	868	1300	2015-06-16 23:21:05.068513+02	\N	\N	\N	f	f	\N
29	900	1200	2015-06-22 15:54:34.466453+02	\N	\N	\N	f	f	\N
30	900	1200	2015-06-22 15:54:55.519425+02	\N	\N	\N	f	f	\N
31	914	1200	2015-06-22 15:55:53.715811+02	\N	\N	\N	f	f	\N
32	801	1200	2015-07-20 21:14:58.380045+02	\N	\N	\N	f	f	\N
33	1667	2500	2015-07-27 00:38:01.84918+02	\N	\N	\N	f	f	\N
34	1250	1900	2015-09-26 21:46:57.13785+02	\N	\N	\N	f	f	\N
35	1250	1900	2015-09-30 07:59:03.795537+02	\N	\N	\N	f	f	\N
36	1400	2100	2016-02-08 10:07:45.046443+01	\N	\N	\N	f	f	\N
37	1600	2100	2016-02-08 10:07:47.10268+01	\N	\N	\N	f	f	\N
38	1080	1920	2016-02-08 10:07:50.594752+01	\N	\N	\N	f	f	\N
\.


--
-- Data for Name: hosting_railsbetauser; Type: TABLE DATA; Schema: public; Owner: app
--

COPY hosting_railsbetauser (id, email, received_date) FROM stdin;
\.


--
-- Name: hosting_railsbetauser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('hosting_railsbetauser_id_seq', 1, false);


--
-- Data for Name: menus_cachekey; Type: TABLE DATA; Schema: public; Owner: app
--

COPY menus_cachekey (id, language, site, key) FROM stdin;
190	en-us	1	menu_cache_menu_nodes_en-us_1
189	en-us	1	menu_cache_menu_nodes_en-us_1_1_user
\.


--
-- Name: menus_cachekey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('menus_cachekey_id_seq', 190, true);


--
-- Data for Name: railshosting_railsbetauser; Type: TABLE DATA; Schema: public; Owner: app
--

COPY railshosting_railsbetauser (id, email, received_date) FROM stdin;
1	info@renuo.ch	2015-06-25 00:34:03.436018+02
2	babedream312@gmx.de	2015-07-23 12:46:59.981695+02
\.


--
-- Name: railshosting_railsbetauser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('railshosting_railsbetauser_id_seq', 2, true);


--
-- Data for Name: reversion_revision; Type: TABLE DATA; Schema: public; Owner: app
--

COPY reversion_revision (id, manager_slug, date_created, comment, user_id) FROM stdin;
1	default	2015-06-12 18:53:01.637515+02	Initial version.	1
2	default	2015-06-12 19:05:57.126279+02	Initial version.	1
3	default	2015-06-12 19:06:25.695064+02	Changed application_urls, application_namespace and xframe_options.	1
4	default	2015-06-12 19:14:13.048438+02	Changed template and xframe_options.	1
6	default	2015-06-12 22:03:12.514876+02	Changed page_title.	1
8	default	2015-06-12 22:06:13.563737+02	Changed menu_title and page_title.	1
9	default	2015-06-12 22:06:55.930234+02	Changed page_title.	1
11	default	2015-06-12 22:17:24.401903+02	Changed page_title.	1
13	default	2015-06-13 15:08:13.293802+02	Template changed to Blog	1
17	default	2015-06-14 05:14:35.039665+02	Changed meta_description.	1
19	default	2015-06-14 05:43:15.812565+02	Changed xframe_options.	1
20	default	2015-06-14 05:43:22.048074+02	No fields changed.	1
22	default	2015-06-14 07:05:22.160184+02	Publish	1
23	default	2015-06-15 15:54:36.304988+02	Publish	1
24	default	2015-06-15 16:05:44.501874+02	Publish	1
25	default	2015-06-16 10:02:34.802098+02	Publish	1
26	default	2015-06-16 10:09:30.848891+02	Publish	1
27	default	2015-06-16 10:21:40.899986+02	Publish	1
28	default	2015-10-04 18:47:36.360447+02	Publish	1
29	default	2015-10-04 19:28:52.058918+02	Publish	1
30	default	2015-10-04 23:27:23.676798+02	Publish	1
31	default	2015-10-04 23:27:56.852619+02	Publish	1
32	default	2015-10-04 23:28:58.369663+02	Publish	1
33	default	2015-10-04 23:34:26.223668+02	Publish	1
34	default	2015-10-05 00:51:13.664439+02	Publish	1
35	default	2015-10-05 00:51:15.361757+02	Publish	1
36	default	2015-10-05 00:51:37.492595+02	Publish	1
37	default	2015-10-05 00:53:00.337511+02	Publish	1
38	default	2015-10-05 00:55:29.733098+02	Publish	1
39	default	2015-10-05 00:55:37.505684+02	Publish	1
40	default	2015-10-05 00:59:54.511074+02	Publish	1
41	default	2015-11-05 08:34:37.101455+01	Publish	1
42	default	2016-02-08 10:37:50.269743+01	Digital Glarus Gallery plugin added to digital_glarus_gallery_grid	1
43	default	2016-02-08 10:37:56.688543+01	Digital Glarus Gallery plugin edited at position 0 in digital_glarus_gallery_grid	1
44	default	2016-02-08 10:38:02.28292+01	Publish	1
45	default	2016-02-08 10:40:46.499548+01	Publish	1
\.


--
-- Name: reversion_revision_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('reversion_revision_id_seq', 45, true);


--
-- Data for Name: reversion_version; Type: TABLE DATA; Schema: public; Owner: app
--

COPY reversion_version (id, object_id, object_id_int, format, serialized_data, object_repr, content_type_id, revision_id) FROM stdin;
1	1	1	json	[{"model": "cms.page", "fields": {"placeholders": [], "languages": "en-us", "changed_date": "2015-06-12T16:53:01.585Z", "revision_id": 0, "depth": 1, "soft_root": false, "login_required": false, "path": "0001", "in_navigation": true, "publication_date": "2015-06-12T16:53:01.463Z", "xframe_options": 0, "creation_date": "2015-06-12T16:53:01.363Z", "navigation_extenders": null, "application_urls": null, "publication_end_date": null, "limit_visibility_in_menu": null, "is_home": true, "application_namespace": null, "reverse_id": null, "changed_by": "ungleich", "created_by": "ungleich", "parent": null, "template": "INHERIT", "numchild": 0, "site": 1}, "pk": 1}]	Home	11	1
2	1	1	json	[{"model": "cms.title", "fields": {"page": 1, "meta_description": "", "language": "en-us", "published": true, "creation_date": "2015-06-12T16:53:01.422Z", "path": "", "redirect": null, "slug": "home", "page_title": "", "menu_title": "", "title": "Home", "has_url_overwrite": false}, "pk": 1}]	Home (home, en-us)	16	1
3	3	3	json	[{"model": "cms.title", "pk": 3, "fields": {"creation_date": "2015-06-12T17:05:57.066Z", "redirect": null, "language": "en-us", "path": "blog", "menu_title": "", "page_title": "", "slug": "blog", "has_url_overwrite": false, "title": "Blog", "meta_description": "", "page": 3, "published": false}}]	Blog (blog, en-us)	16	2
4	3	3	json	[{"model": "cms.page", "pk": 3, "fields": {"depth": 1, "path": "0003", "revision_id": 0, "application_urls": null, "xframe_options": 0, "placeholders": [6], "site": 1, "soft_root": false, "languages": "en-us", "limit_visibility_in_menu": null, "changed_date": "2015-06-12T17:05:57.068Z", "publication_date": null, "reverse_id": null, "is_home": false, "changed_by": "ungleich", "publication_end_date": null, "creation_date": "2015-06-12T17:05:57.028Z", "login_required": false, "parent": null, "template": "INHERIT", "application_namespace": null, "navigation_extenders": null, "in_navigation": true, "created_by": "ungleich", "numchild": 0}}]	Blog	11	2
5	6	6	json	[{"model": "cms.placeholder", "pk": 6, "fields": {"default_width": null, "slot": "page_content"}}]	page_content	9	2
6	3	3	json	[{"model": "cms.title", "pk": 3, "fields": {"creation_date": "2015-06-12T17:05:57.066Z", "redirect": "", "language": "en-us", "path": "blog", "menu_title": "", "page_title": "", "slug": "blog", "has_url_overwrite": false, "title": "Blog", "meta_description": "", "page": 3, "published": false}}]	Blog (blog, en-us)	16	3
7	3	3	json	[{"model": "cms.page", "pk": 3, "fields": {"depth": 1, "path": "0003", "revision_id": 0, "application_urls": "BlogApp", "xframe_options": 0, "placeholders": [6], "site": 1, "soft_root": false, "languages": "en-us", "limit_visibility_in_menu": null, "changed_date": "2015-06-12T17:06:25.648Z", "publication_date": null, "reverse_id": null, "is_home": false, "changed_by": "ungleich", "publication_end_date": null, "creation_date": "2015-06-12T17:05:57.028Z", "login_required": false, "parent": null, "template": "INHERIT", "application_namespace": "djangocms_blog", "navigation_extenders": "", "in_navigation": true, "created_by": "ungleich", "numchild": 0}}]	Blog	11	3
8	6	6	json	[{"model": "cms.placeholder", "pk": 6, "fields": {"default_width": null, "slot": "page_content"}}]	page_content	9	3
9	3	3	json	[{"pk": 3, "model": "cms.title", "fields": {"slug": "blog", "meta_description": "", "menu_title": "", "published": false, "title": "Blog", "has_url_overwrite": false, "redirect": "", "path": "blog", "creation_date": "2015-06-12T17:05:57.066Z", "language": "en-us", "page_title": "", "page": 3}}]	Blog (blog, en-us)	16	4
10	3	3	json	[{"pk": 3, "model": "cms.page", "fields": {"limit_visibility_in_menu": null, "created_by": "ungleich", "soft_root": false, "parent": null, "changed_by": "ungleich", "navigation_extenders": "", "login_required": false, "changed_date": "2015-06-12T17:14:12.988Z", "path": "0003", "creation_date": "2015-06-12T17:05:57.028Z", "numchild": 0, "publication_end_date": null, "in_navigation": true, "languages": "en-us", "reverse_id": null, "placeholders": [6], "publication_date": null, "revision_id": 0, "application_namespace": "djangocms_blog", "site": 1, "depth": 1, "template": "cms/ungleich.ch/blog.html", "xframe_options": 0, "is_home": false, "application_urls": "BlogApp"}}]	Blog	11	4
11	6	6	json	[{"pk": 6, "model": "cms.placeholder", "fields": {"slot": "page_content", "default_width": null}}]	page_content	9	4
16	3	3	json	[{"pk": 3, "fields": {"has_url_overwrite": false, "meta_description": "", "page": 3, "path": "blog", "language": "en-us", "published": true, "slug": "blog", "title": "Blog", "redirect": "", "creation_date": "2015-06-12T17:05:57.066Z", "page_title": "ungleich Blog", "menu_title": ""}, "model": "cms.title"}]	Blog (blog, en-us)	16	6
17	3	3	json	[{"pk": 3, "fields": {"created_by": "ungleich", "site": 1, "path": "0003", "xframe_options": 0, "depth": 1, "navigation_extenders": "", "login_required": false, "languages": "en-us", "creation_date": "2015-06-12T17:05:57.028Z", "reverse_id": null, "revision_id": 0, "application_namespace": "djangocms_blog", "in_navigation": true, "changed_by": "ungleich", "placeholders": [6], "application_urls": "BlogApp", "publication_end_date": null, "soft_root": false, "changed_date": "2015-06-12T20:03:12.429Z", "publication_date": "2015-06-12T17:17:49.261Z", "is_home": false, "parent": null, "limit_visibility_in_menu": null, "numchild": 0, "template": "cms/ungleich.ch/blog.html"}, "model": "cms.page"}]	Blog	11	6
18	6	6	json	[{"pk": 6, "fields": {"default_width": null, "slot": "page_content"}, "model": "cms.placeholder"}]	page_content	9	6
22	3	3	json	[{"pk": 3, "fields": {"has_url_overwrite": false, "meta_description": "", "page": 3, "path": "blog", "language": "en-us", "published": true, "slug": "blog", "title": "Blog", "redirect": "", "creation_date": "2015-06-12T17:05:57.066Z", "page_title": "Ungleich blog", "menu_title": "Blog"}, "model": "cms.title"}]	Blog (blog, en-us)	16	8
23	3	3	json	[{"pk": 3, "fields": {"created_by": "ungleich", "site": 1, "path": "0003", "xframe_options": 0, "depth": 1, "navigation_extenders": "", "login_required": false, "languages": "en-us", "creation_date": "2015-06-12T17:05:57.028Z", "reverse_id": null, "revision_id": 0, "application_namespace": "djangocms_blog", "in_navigation": true, "changed_by": "ungleich", "placeholders": [6], "application_urls": "BlogApp", "publication_end_date": null, "soft_root": false, "changed_date": "2015-06-12T20:06:13.520Z", "publication_date": "2015-06-12T17:17:49.261Z", "is_home": false, "parent": null, "limit_visibility_in_menu": null, "numchild": 0, "template": "cms/ungleich.ch/blog.html"}, "model": "cms.page"}]	Blog	11	8
24	6	6	json	[{"pk": 6, "fields": {"default_width": null, "slot": "page_content"}, "model": "cms.placeholder"}]	page_content	9	8
25	3	3	json	[{"pk": 3, "fields": {"has_url_overwrite": false, "meta_description": "", "page": 3, "path": "blog", "language": "en-us", "published": true, "slug": "blog", "title": "Blog", "redirect": "", "creation_date": "2015-06-12T17:05:57.066Z", "page_title": "Ungleich Blog", "menu_title": "Blog"}, "model": "cms.title"}]	Blog (blog, en-us)	16	9
26	3	3	json	[{"pk": 3, "fields": {"created_by": "ungleich", "site": 1, "path": "0003", "xframe_options": 0, "depth": 1, "navigation_extenders": "", "login_required": false, "languages": "en-us", "creation_date": "2015-06-12T17:05:57.028Z", "reverse_id": null, "revision_id": 0, "application_namespace": "djangocms_blog", "in_navigation": true, "changed_by": "ungleich", "placeholders": [6], "application_urls": "BlogApp", "publication_end_date": null, "soft_root": false, "changed_date": "2015-06-12T20:06:55.883Z", "publication_date": "2015-06-12T17:17:49.261Z", "is_home": false, "parent": null, "limit_visibility_in_menu": null, "numchild": 0, "template": "cms/ungleich.ch/blog.html"}, "model": "cms.page"}]	Blog	11	9
27	6	6	json	[{"pk": 6, "fields": {"default_width": null, "slot": "page_content"}, "model": "cms.placeholder"}]	page_content	9	9
31	3	3	json	[{"pk": 3, "fields": {"has_url_overwrite": false, "meta_description": "", "page": 3, "path": "blog", "language": "en-us", "published": true, "slug": "blog", "title": "Blog", "redirect": "", "creation_date": "2015-06-12T17:05:57.066Z", "page_title": "ungleich Blog", "menu_title": "Blog"}, "model": "cms.title"}]	Blog (blog, en-us)	16	11
32	3	3	json	[{"pk": 3, "fields": {"created_by": "ungleich", "site": 1, "path": "0003", "xframe_options": 0, "depth": 1, "navigation_extenders": "", "login_required": false, "languages": "en-us", "creation_date": "2015-06-12T17:05:57.028Z", "reverse_id": null, "revision_id": 0, "application_namespace": "djangocms_blog", "in_navigation": true, "changed_by": "ungleich", "placeholders": [6], "application_urls": "BlogApp", "publication_end_date": null, "soft_root": false, "changed_date": "2015-06-12T20:17:24.358Z", "publication_date": "2015-06-12T17:17:49.261Z", "is_home": false, "parent": null, "limit_visibility_in_menu": null, "numchild": 0, "template": "cms/ungleich.ch/blog.html"}, "model": "cms.page"}]	Blog	11	11
33	6	6	json	[{"pk": 6, "fields": {"default_width": null, "slot": "page_content"}, "model": "cms.placeholder"}]	page_content	9	11
37	3	3	json	[{"pk": 3, "fields": {"has_url_overwrite": false, "meta_description": "", "page": 3, "path": "blog", "language": "en-us", "published": true, "slug": "blog", "title": "Blog", "redirect": "", "creation_date": "2015-06-12T17:05:57.066Z", "page_title": "ungleich Blog", "menu_title": "Blog"}, "model": "cms.title"}]	Blog (blog, en-us)	16	13
38	3	3	json	[{"pk": 3, "fields": {"created_by": "ungleich", "site": 1, "path": "0003", "xframe_options": 0, "depth": 1, "navigation_extenders": "", "login_required": false, "languages": "en-us", "creation_date": "2015-06-12T17:05:57.028Z", "reverse_id": null, "revision_id": 0, "application_namespace": "djangocms_blog", "in_navigation": true, "changed_by": "ungleich", "placeholders": [6], "application_urls": "BlogApp", "publication_end_date": null, "soft_root": false, "changed_date": "2015-06-13T13:08:13.077Z", "publication_date": "2015-06-12T17:17:49.261Z", "is_home": false, "parent": null, "limit_visibility_in_menu": null, "numchild": 0, "template": "cms/ungleich.ch/blog.html"}, "model": "cms.page"}]	Blog	11	13
39	6	6	json	[{"pk": 6, "fields": {"default_width": null, "slot": "page_content"}, "model": "cms.placeholder"}]	page_content	9	13
49	3	3	json	[{"pk": 3, "fields": {"title": "Blog", "language": "en-us", "published": true, "page_title": "ungleich Blog", "has_url_overwrite": false, "page": 3, "meta_description": "on OpenSource, technology, our passion and interests...", "creation_date": "2015-06-12T17:05:57.066Z", "menu_title": "Blog", "slug": "blog", "path": "blog", "redirect": ""}, "model": "cms.title"}]	Blog (blog, en-us)	16	17
50	3	3	json	[{"pk": 3, "fields": {"placeholders": [6], "template": "cms/ungleich.ch/blog.html", "application_namespace": "djangocms_blog", "created_by": "ungleich", "changed_by": "ungleich", "xframe_options": 0, "is_home": false, "site": 1, "limit_visibility_in_menu": null, "navigation_extenders": "", "changed_date": "2015-06-14T03:14:34.984Z", "reverse_id": null, "languages": "en-us", "login_required": false, "revision_id": 0, "soft_root": false, "creation_date": "2015-06-12T17:05:57.028Z", "parent": null, "depth": 1, "publication_date": "2015-06-12T17:17:49.261Z", "numchild": 0, "in_navigation": true, "path": "0003", "application_urls": "BlogApp", "publication_end_date": null}, "model": "cms.page"}]	Blog	11	17
51	6	6	json	[{"pk": 6, "fields": {"default_width": null, "slot": "page_content"}, "model": "cms.placeholder"}]	page_content	9	17
55	3	3	json	[{"pk": 3, "fields": {"title": "Blog", "language": "en-us", "published": true, "page_title": "ungleich Blog", "has_url_overwrite": false, "page": 3, "meta_description": "on OpenSource, technology, our passion and interests...", "creation_date": "2015-06-12T17:05:57.066Z", "menu_title": "Blog", "slug": "blog", "path": "blog", "redirect": ""}, "model": "cms.title"}]	Blog (blog, en-us)	16	19
56	3	3	json	[{"pk": 3, "fields": {"placeholders": [6], "template": "cms/ungleich.ch/blog.html", "application_namespace": "djangocms_blog", "created_by": "ungleich", "changed_by": "ungleich", "xframe_options": 0, "is_home": false, "site": 1, "limit_visibility_in_menu": null, "navigation_extenders": "", "changed_date": "2015-06-14T03:43:15.769Z", "reverse_id": null, "languages": "en-us", "login_required": false, "revision_id": 0, "soft_root": false, "creation_date": "2015-06-12T17:05:57.028Z", "parent": null, "depth": 1, "publication_date": "2015-06-12T17:17:49.261Z", "numchild": 0, "in_navigation": true, "path": "0003", "application_urls": "BlogApp", "publication_end_date": null}, "model": "cms.page"}]	Blog	11	19
57	6	6	json	[{"pk": 6, "fields": {"default_width": null, "slot": "page_content"}, "model": "cms.placeholder"}]	page_content	9	19
58	3	3	json	[{"pk": 3, "fields": {"title": "Blog", "language": "en-us", "published": true, "page_title": "ungleich Blog", "has_url_overwrite": false, "page": 3, "meta_description": "on OpenSource, technology, our passion and interests...", "creation_date": "2015-06-12T17:05:57.066Z", "menu_title": "Blog", "slug": "blog", "path": "blog", "redirect": ""}, "model": "cms.title"}]	Blog (blog, en-us)	16	20
59	3	3	json	[{"pk": 3, "fields": {"placeholders": [6], "template": "cms/ungleich.ch/blog.html", "application_namespace": "djangocms_blog", "created_by": "ungleich", "changed_by": "ungleich", "xframe_options": 0, "is_home": false, "site": 1, "limit_visibility_in_menu": null, "navigation_extenders": "", "changed_date": "2015-06-14T03:43:22.004Z", "reverse_id": null, "languages": "en-us", "login_required": false, "revision_id": 0, "soft_root": false, "creation_date": "2015-06-12T17:05:57.028Z", "parent": null, "depth": 1, "publication_date": "2015-06-12T17:17:49.261Z", "numchild": 0, "in_navigation": true, "path": "0003", "application_urls": "BlogApp", "publication_end_date": null}, "model": "cms.page"}]	Blog	11	20
60	6	6	json	[{"pk": 6, "fields": {"default_width": null, "slot": "page_content"}, "model": "cms.placeholder"}]	page_content	9	20
64	3	3	json	[{"fields": {"page_title": "ungleich Blog", "page": 3, "has_url_overwrite": false, "redirect": "", "meta_description": "on OpenSource, technology, our passion and interests...", "title": "Blog", "menu_title": "Blog", "published": true, "slug": "blog", "path": "blog", "language": "en-us", "creation_date": "2015-06-12T17:05:57.066Z"}, "pk": 3, "model": "cms.title"}]	Blog (blog, en-us)	16	22
65	3	3	json	[{"fields": {"limit_visibility_in_menu": null, "depth": 1, "publication_end_date": null, "creation_date": "2015-06-12T17:05:57.028Z", "revision_id": 0, "template": "cms/ungleich.ch/blog.html", "soft_root": false, "reverse_id": null, "languages": "en-us", "path": "0003", "is_home": false, "changed_by": "ungleich", "application_urls": "BlogApp", "site": 1, "xframe_options": 0, "in_navigation": false, "placeholders": [6], "parent": null, "login_required": false, "application_namespace": "djangocms_blog", "created_by": "ungleich", "publication_date": "2015-06-12T17:17:49.261Z", "navigation_extenders": "", "numchild": 0, "changed_date": "2015-06-14T05:05:22.108Z"}, "pk": 3, "model": "cms.page"}]	Blog	11	22
66	6	6	json	[{"fields": {"slot": "page_content", "default_width": null}, "pk": 6, "model": "cms.placeholder"}]	page_content	9	22
67	3	3	json	[{"fields": {"page_title": "ungleich Blog", "page": 3, "has_url_overwrite": false, "redirect": "", "meta_description": "on OpenSource, technology, our passion and interests...", "title": "Blog", "menu_title": "Blog", "published": true, "slug": "blog", "path": "blog", "language": "en-us", "creation_date": "2015-06-12T17:05:57.066Z"}, "pk": 3, "model": "cms.title"}]	Blog (blog, en-us)	16	23
68	3	3	json	[{"fields": {"limit_visibility_in_menu": null, "depth": 1, "publication_end_date": null, "creation_date": "2015-06-12T17:05:57.028Z", "revision_id": 0, "template": "cms/ungleich.ch/blog.html", "soft_root": false, "reverse_id": null, "languages": "en-us", "path": "0003", "is_home": false, "changed_by": "ungleich", "application_urls": "BlogApp", "site": 1, "xframe_options": 0, "in_navigation": false, "placeholders": [6], "parent": null, "login_required": false, "application_namespace": "djangocms_blog", "created_by": "ungleich", "publication_date": "2015-06-12T17:17:49.261Z", "navigation_extenders": "", "numchild": 0, "changed_date": "2015-06-15T13:54:36.210Z"}, "pk": 3, "model": "cms.page"}]	Blog	11	23
69	6	6	json	[{"fields": {"slot": "page_content", "default_width": null}, "pk": 6, "model": "cms.placeholder"}]	page_content	9	23
90	28	28	json	[{"model": "cms.placeholder", "fields": {"default_width": null, "slot": "digital_glarus_where_we_are_content"}, "pk": 28}]	digital_glarus_where_we_are_content	9	28
70	3	3	json	[{"fields": {"page_title": "ungleich Blog", "page": 3, "has_url_overwrite": false, "redirect": "", "meta_description": "on OpenSource, technology, our passion and interests...", "title": "Blog", "menu_title": "Blog", "published": true, "slug": "blog", "path": "blog", "language": "en-us", "creation_date": "2015-06-12T17:05:57.066Z"}, "pk": 3, "model": "cms.title"}]	Blog (blog, en-us)	16	24
71	3	3	json	[{"fields": {"limit_visibility_in_menu": null, "depth": 1, "publication_end_date": null, "creation_date": "2015-06-12T17:05:57.028Z", "revision_id": 0, "template": "cms/ungleich.ch/blog.html", "soft_root": false, "reverse_id": null, "languages": "en-us", "path": "0003", "is_home": false, "changed_by": "ungleich", "application_urls": "BlogApp", "site": 1, "xframe_options": 0, "in_navigation": false, "placeholders": [6], "parent": null, "login_required": false, "application_namespace": "djangocms_blog", "created_by": "ungleich", "publication_date": "2015-06-12T17:17:49.261Z", "navigation_extenders": "", "numchild": 0, "changed_date": "2015-06-15T14:05:44.415Z"}, "pk": 3, "model": "cms.page"}]	Blog	11	24
72	6	6	json	[{"fields": {"slot": "page_content", "default_width": null}, "pk": 6, "model": "cms.placeholder"}]	page_content	9	24
73	3	3	json	[{"pk": 3, "fields": {"meta_description": "on OpenSource, technology, our passion and interests...", "creation_date": "2015-06-12T17:05:57.066Z", "slug": "blog", "page": 3, "page_title": "ungleich Blog", "language": "en-us", "published": true, "menu_title": "Blog", "title": "Blog", "has_url_overwrite": false, "redirect": "", "path": "blog"}, "model": "cms.title"}]	Blog (blog, en-us)	16	25
74	3	3	json	[{"pk": 3, "fields": {"revision_id": 0, "in_navigation": false, "creation_date": "2015-06-12T17:05:57.028Z", "publication_date": "2015-06-12T17:17:49.261Z", "xframe_options": 0, "created_by": "ungleich", "publication_end_date": null, "parent": null, "reverse_id": null, "placeholders": [6], "login_required": false, "site": 1, "changed_by": "ungleich", "changed_date": "2015-06-16T08:02:34.712Z", "application_namespace": "djangocms_blog", "soft_root": false, "limit_visibility_in_menu": null, "numchild": 0, "application_urls": "BlogApp", "depth": 1, "languages": "en-us", "template": "cms/ungleich.ch/blog.html", "path": "0003", "is_home": false, "navigation_extenders": ""}, "model": "cms.page"}]	Blog	11	25
75	6	6	json	[{"pk": 6, "fields": {"slot": "page_content", "default_width": null}, "model": "cms.placeholder"}]	page_content	9	25
76	3	3	json	[{"pk": 3, "fields": {"meta_description": "on OpenSource, technology, our passion and interests...", "creation_date": "2015-06-12T17:05:57.066Z", "slug": "blog", "page": 3, "page_title": "ungleich Blog", "language": "en-us", "published": true, "menu_title": "Blog", "title": "Blog", "has_url_overwrite": false, "redirect": "", "path": "blog"}, "model": "cms.title"}]	Blog (blog, en-us)	16	26
77	3	3	json	[{"pk": 3, "fields": {"revision_id": 0, "in_navigation": false, "creation_date": "2015-06-12T17:05:57.028Z", "publication_date": "2015-06-12T17:17:49.261Z", "xframe_options": 0, "created_by": "ungleich", "publication_end_date": null, "parent": null, "reverse_id": null, "placeholders": [6], "login_required": false, "site": 1, "changed_by": "ungleich", "changed_date": "2015-06-16T08:09:30.776Z", "application_namespace": "djangocms_blog", "soft_root": false, "limit_visibility_in_menu": null, "numchild": 0, "application_urls": "BlogApp", "depth": 1, "languages": "en-us", "template": "cms/ungleich.ch/blog.html", "path": "0003", "is_home": false, "navigation_extenders": ""}, "model": "cms.page"}]	Blog	11	26
78	6	6	json	[{"pk": 6, "fields": {"slot": "page_content", "default_width": null}, "model": "cms.placeholder"}]	page_content	9	26
79	3	3	json	[{"pk": 3, "fields": {"meta_description": "on OpenSource, technology, our passion and interests...", "creation_date": "2015-06-12T17:05:57.066Z", "slug": "blog", "page": 3, "page_title": "ungleich Blog", "language": "en-us", "published": true, "menu_title": "Blog", "title": "Blog", "has_url_overwrite": false, "redirect": "", "path": "blog"}, "model": "cms.title"}]	Blog (blog, en-us)	16	27
80	3	3	json	[{"pk": 3, "fields": {"revision_id": 0, "in_navigation": false, "creation_date": "2015-06-12T17:05:57.028Z", "publication_date": "2015-06-12T17:17:49.261Z", "xframe_options": 0, "created_by": "ungleich", "publication_end_date": null, "parent": null, "reverse_id": null, "placeholders": [6], "login_required": false, "site": 1, "changed_by": "ungleich", "changed_date": "2015-06-16T08:21:40.825Z", "application_namespace": "djangocms_blog", "soft_root": false, "limit_visibility_in_menu": null, "numchild": 0, "application_urls": "BlogApp", "depth": 1, "languages": "en-us", "template": "cms/ungleich.ch/blog.html", "path": "0003", "is_home": false, "navigation_extenders": ""}, "model": "cms.page"}]	Blog	11	27
81	6	6	json	[{"pk": 6, "fields": {"slot": "page_content", "default_width": null}, "model": "cms.placeholder"}]	page_content	9	27
82	5	5	json	[{"model": "cms.title", "fields": {"creation_date": "2015-10-04T16:27:41.449Z", "slug": "digital-glarus-home", "meta_description": "", "page_title": "Digital Glarus", "menu_title": "home", "redirect": "", "path": "diigtalglarus2", "title": "digital glarus home", "has_url_overwrite": true, "language": "en-us", "page": 5, "published": true}, "pk": 5}]	digital glarus home (digital-glarus-home, en-us)	16	28
83	5	5	json	[{"model": "cms.page", "fields": {"application_namespace": null, "soft_root": false, "publication_end_date": null, "created_by": "ungleich", "changed_by": "ungleich", "path": "0005", "template": "cms/digitalglarus/index.html", "site": 1, "reverse_id": null, "is_home": false, "navigation_extenders": "", "depth": 1, "creation_date": "2015-10-04T16:27:41.288Z", "application_urls": "", "login_required": false, "publication_date": "2015-10-04T16:47:36.159Z", "numchild": 0, "limit_visibility_in_menu": null, "revision_id": 0, "parent": null, "in_navigation": true, "placeholders": [21, 22, 23, 24, 25, 26, 27, 28, 29], "languages": "en-us", "xframe_options": 0, "changed_date": "2015-10-04T16:47:36.284Z"}, "pk": 5}]	home	11	28
84	22	22	json	[{"model": "cms.placeholder", "fields": {"default_width": null, "slot": "digital_glarus_build_a_tech_valley_content"}, "pk": 22}]	digital_glarus_build_a_tech_valley_content	9	28
85	23	23	json	[{"model": "cms.placeholder", "fields": {"default_width": null, "slot": "digital_glarus_a_new_area"}, "pk": 23}]	digital_glarus_a_new_area	9	28
86	24	24	json	[{"model": "cms.placeholder", "fields": {"default_width": null, "slot": "digital_glarus_a_new_area_content"}, "pk": 24}]	digital_glarus_a_new_area_content	9	28
87	25	25	json	[{"model": "cms.placeholder", "fields": {"default_width": null, "slot": "digital_glarus_why_be_interested"}, "pk": 25}]	digital_glarus_why_be_interested	9	28
88	26	26	json	[{"model": "cms.placeholder", "fields": {"default_width": null, "slot": "digital_glarus_why_be_interested_content"}, "pk": 26}]	digital_glarus_why_be_interested_content	9	28
89	27	27	json	[{"model": "cms.placeholder", "fields": {"default_width": null, "slot": "digital_glarus_where_we_are"}, "pk": 27}]	digital_glarus_where_we_are	9	28
91	29	29	json	[{"model": "cms.placeholder", "fields": {"default_width": null, "slot": "digital_glarus_legend"}, "pk": 29}]	digital_glarus_legend	9	28
92	21	21	json	[{"model": "cms.placeholder", "fields": {"default_width": null, "slot": "digital_glarus_build_a_tech_valley"}, "pk": 21}]	digital_glarus_build_a_tech_valley	9	28
93	3	3	json	[{"model": "cms.title", "fields": {"creation_date": "2015-06-12T17:05:57.066Z", "slug": "blog", "meta_description": "on OpenSource, technology, our passion and interests...", "page_title": "ungleich Blog", "menu_title": "Blog", "redirect": "", "path": "blog", "title": "Blog", "has_url_overwrite": true, "language": "en-us", "page": 3, "published": true}, "pk": 3}]	Blog (blog, en-us)	16	29
94	3	3	json	[{"model": "cms.page", "fields": {"application_namespace": "djangocms_blog", "soft_root": false, "publication_end_date": null, "created_by": "ungleich", "changed_by": "ungleich", "path": "0003", "template": "cms/ungleichch/blog.html", "site": 1, "reverse_id": null, "is_home": false, "navigation_extenders": "", "depth": 1, "creation_date": "2015-06-12T17:05:57.028Z", "application_urls": "BlogApp", "login_required": false, "publication_date": "2015-06-12T17:17:49.261Z", "numchild": 0, "limit_visibility_in_menu": null, "revision_id": 0, "parent": null, "in_navigation": false, "placeholders": [6], "languages": "en-us", "xframe_options": 0, "changed_date": "2015-10-04T17:28:51.984Z"}, "pk": 3}]	Blog	11	29
95	6	6	json	[{"model": "cms.placeholder", "fields": {"default_width": null, "slot": "page_content"}, "pk": 6}]	page_content	9	29
96	64	64	json	[{"pk": 64, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_where_we_are_content", "default_width": null}}]	digital_glarus_where_we_are_content	9	30
97	65	65	json	[{"pk": 65, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_legend", "default_width": null}}]	digital_glarus_legend	9	30
98	7	7	json	[{"pk": 7, "model": "cms.title", "fields": {"slug": "fooffff", "page_title": "ffff", "title": "fooffff", "meta_description": "ffffff", "language": "en-us", "creation_date": "2015-10-04T21:22:33.989Z", "menu_title": "ffff", "redirect": null, "published": true, "path": "diigtalglarus2/fooffff", "page": 8, "has_url_overwrite": false}}]	fooffff (fooffff, en-us)	16	30
99	8	8	json	[{"pk": 8, "model": "cms.page", "fields": {"depth": 2, "numchild": 0, "limit_visibility_in_menu": null, "in_navigation": true, "publication_end_date": null, "application_namespace": null, "publication_date": "2015-10-04T21:27:23.416Z", "login_required": false, "application_urls": null, "reverse_id": null, "soft_root": false, "parent": 5, "is_home": false, "site": 1, "changed_date": "2015-10-04T21:27:23.557Z", "xframe_options": 0, "creation_date": "2015-10-04T21:22:33.837Z", "changed_by": "ungleich", "created_by": "ungleich", "languages": "en-us", "placeholders": [57, 58, 59, 60, 61, 62, 63, 64, 65], "revision_id": 0, "path": "00050001", "template": "INHERIT", "navigation_extenders": null}}]	ffff	11	30
100	57	57	json	[{"pk": 57, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_build_a_tech_valley", "default_width": null}}]	digital_glarus_build_a_tech_valley	9	30
101	58	58	json	[{"pk": 58, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_build_a_tech_valley_content", "default_width": null}}]	digital_glarus_build_a_tech_valley_content	9	30
102	59	59	json	[{"pk": 59, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_a_new_area", "default_width": null}}]	digital_glarus_a_new_area	9	30
103	60	60	json	[{"pk": 60, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_a_new_area_content", "default_width": null}}]	digital_glarus_a_new_area_content	9	30
104	61	61	json	[{"pk": 61, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_why_be_interested", "default_width": null}}]	digital_glarus_why_be_interested	9	30
105	62	62	json	[{"pk": 62, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_why_be_interested_content", "default_width": null}}]	digital_glarus_why_be_interested_content	9	30
106	63	63	json	[{"pk": 63, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_where_we_are", "default_width": null}}]	digital_glarus_where_we_are	9	30
107	81	81	json	[{"pk": 81, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_build_a_tech_valley", "default_width": null}}]	digital_glarus_build_a_tech_valley	9	31
108	82	82	json	[{"pk": 82, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_build_a_tech_valley_content", "default_width": null}}]	digital_glarus_build_a_tech_valley_content	9	31
109	83	83	json	[{"pk": 83, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_a_new_area", "default_width": null}}]	digital_glarus_a_new_area	9	31
110	84	84	json	[{"pk": 84, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_a_new_area_content", "default_width": null}}]	digital_glarus_a_new_area_content	9	31
111	85	85	json	[{"pk": 85, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_why_be_interested", "default_width": null}}]	digital_glarus_why_be_interested	9	31
112	86	86	json	[{"pk": 86, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_why_be_interested_content", "default_width": null}}]	digital_glarus_why_be_interested_content	9	31
113	87	87	json	[{"pk": 87, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_where_we_are", "default_width": null}}]	digital_glarus_where_we_are	9	31
114	88	88	json	[{"pk": 88, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_where_we_are_content", "default_width": null}}]	digital_glarus_where_we_are_content	9	31
115	9	9	json	[{"pk": 9, "model": "cms.page", "fields": {"depth": 2, "numchild": 0, "limit_visibility_in_menu": null, "in_navigation": true, "publication_end_date": null, "application_namespace": null, "publication_date": "2015-10-04T21:27:56.742Z", "login_required": false, "application_urls": null, "reverse_id": null, "soft_root": false, "parent": 5, "is_home": false, "site": 1, "changed_date": "2015-10-04T21:27:56.823Z", "xframe_options": 0, "creation_date": "2015-10-04T21:22:53.644Z", "changed_by": "ungleich", "created_by": "ungleich", "languages": "en-us", "placeholders": [81, 82, 83, 84, 85, 86, 87, 88, 89], "revision_id": 0, "path": "00050002", "template": "INHERIT", "navigation_extenders": null}}]	cccccccccccccc	11	31
116	8	8	json	[{"pk": 8, "model": "cms.title", "fields": {"slug": "ccccccccccccc", "page_title": "ccccccccccccccccc", "title": "ccccccccccccc", "meta_description": "ccc", "language": "en-us", "creation_date": "2015-10-04T21:22:53.668Z", "menu_title": "cccccccccccccc", "redirect": null, "published": true, "path": "diigtalglarus2/ccccccccccccc", "page": 9, "has_url_overwrite": false}}]	ccccccccccccc (ccccccccccccc, en-us)	16	31
117	89	89	json	[{"pk": 89, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_legend", "default_width": null}}]	digital_glarus_legend	9	31
226	76	76	json	[{"pk": 76, "fields": {"dgGallery": 1}, "model": "digitalglarus.dggalleryplugin"}]	76	65	43
118	5	5	json	[{"pk": 5, "model": "cms.title", "fields": {"slug": "digital-glarus-home", "page_title": "Digital Glarus", "title": "digital glarus home", "meta_description": "", "language": "en-us", "creation_date": "2015-10-04T16:27:41.449Z", "menu_title": "home", "redirect": "", "published": true, "path": "diigtalglarus", "page": 5, "has_url_overwrite": true}}]	digital glarus home (digital-glarus-home, en-us)	16	32
119	5	5	json	[{"pk": 5, "model": "cms.page", "fields": {"depth": 1, "numchild": 2, "limit_visibility_in_menu": null, "in_navigation": true, "publication_end_date": null, "application_namespace": null, "publication_date": "2015-10-04T16:47:36.159Z", "login_required": false, "application_urls": "", "reverse_id": null, "soft_root": true, "parent": null, "is_home": false, "site": 1, "changed_date": "2015-10-04T21:28:58.317Z", "xframe_options": 0, "creation_date": "2015-10-04T16:27:41.288Z", "changed_by": "ungleich", "created_by": "ungleich", "languages": "en-us", "placeholders": [21, 22, 23, 24, 25, 26, 27, 28, 29], "revision_id": 0, "path": "0005", "template": "cms/digitalglarus/index.html", "navigation_extenders": ""}}]	home	11	32
120	22	22	json	[{"pk": 22, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_build_a_tech_valley_content", "default_width": null}}]	digital_glarus_build_a_tech_valley_content	9	32
121	23	23	json	[{"pk": 23, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_a_new_area", "default_width": null}}]	digital_glarus_a_new_area	9	32
122	24	24	json	[{"pk": 24, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_a_new_area_content", "default_width": null}}]	digital_glarus_a_new_area_content	9	32
123	25	25	json	[{"pk": 25, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_why_be_interested", "default_width": null}}]	digital_glarus_why_be_interested	9	32
124	26	26	json	[{"pk": 26, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_why_be_interested_content", "default_width": null}}]	digital_glarus_why_be_interested_content	9	32
125	27	27	json	[{"pk": 27, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_where_we_are", "default_width": null}}]	digital_glarus_where_we_are	9	32
126	28	28	json	[{"pk": 28, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_where_we_are_content", "default_width": null}}]	digital_glarus_where_we_are_content	9	32
127	29	29	json	[{"pk": 29, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_legend", "default_width": null}}]	digital_glarus_legend	9	32
128	21	21	json	[{"pk": 21, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_build_a_tech_valley", "default_width": null}}]	digital_glarus_build_a_tech_valley	9	32
129	32	32	json	[{"pk": 32, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_a_new_area", "default_width": null}}]	digital_glarus_a_new_area	9	33
130	1	1	json	[{"pk": 1, "model": "cms.page", "fields": {"depth": 1, "numchild": 0, "limit_visibility_in_menu": null, "in_navigation": false, "publication_end_date": null, "application_namespace": null, "publication_date": "2015-06-12T16:53:01.463Z", "login_required": false, "application_urls": null, "reverse_id": null, "soft_root": false, "parent": null, "is_home": true, "site": 1, "changed_date": "2015-10-04T21:34:26.168Z", "xframe_options": 0, "creation_date": "2015-06-12T16:53:01.363Z", "changed_by": "ungleich", "created_by": "ungleich", "languages": "en-us", "placeholders": [5, 30, 31, 32, 33, 34, 35, 36, 37, 38, 99, 100, 101, 102, 103, 104], "revision_id": 0, "path": "0001", "template": "INHERIT", "navigation_extenders": null}}]	Home	11	33
131	34	34	json	[{"pk": 34, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_why_be_interested", "default_width": null}}]	digital_glarus_why_be_interested	9	33
132	35	35	json	[{"pk": 35, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_why_be_interested_content", "default_width": null}}]	digital_glarus_why_be_interested_content	9	33
133	36	36	json	[{"pk": 36, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_where_we_are", "default_width": null}}]	digital_glarus_where_we_are	9	33
134	5	5	json	[{"pk": 5, "model": "cms.placeholder", "fields": {"slot": "page_content", "default_width": null}}]	page_content	9	33
135	38	38	json	[{"pk": 38, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_legend", "default_width": null}}]	digital_glarus_legend	9	33
136	33	33	json	[{"pk": 33, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_a_new_area_content", "default_width": null}}]	digital_glarus_a_new_area_content	9	33
137	104	104	json	[{"pk": 104, "model": "cms.placeholder", "fields": {"slot": "digitalglarus_why_glarus_direct_connection_zurich", "default_width": null}}]	digitalglarus_why_glarus_direct_connection_zurich	9	33
138	103	103	json	[{"pk": 103, "model": "cms.placeholder", "fields": {"slot": "digitalglarus_why_glarus_affordable_price", "default_width": null}}]	digitalglarus_why_glarus_affordable_price	9	33
139	37	37	json	[{"pk": 37, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_where_we_are_content", "default_width": null}}]	digital_glarus_where_we_are_content	9	33
140	99	99	json	[{"pk": 99, "model": "cms.placeholder", "fields": {"slot": "digitalglarus_why_us", "default_width": null}}]	digitalglarus_why_us	9	33
141	1	1	json	[{"pk": 1, "model": "cms.title", "fields": {"slug": "home", "page_title": "", "title": "Home", "meta_description": "", "language": "en-us", "creation_date": "2015-06-12T16:53:01.422Z", "menu_title": "", "redirect": null, "published": true, "path": "", "page": 1, "has_url_overwrite": false}}]	Home (home, en-us)	16	33
142	100	100	json	[{"pk": 100, "model": "cms.placeholder", "fields": {"slot": "digitalglarus_why_us_content", "default_width": null}}]	digitalglarus_why_us_content	9	33
143	101	101	json	[{"pk": 101, "model": "cms.placeholder", "fields": {"slot": "digitalglarus_why_glarus", "default_width": null}}]	digitalglarus_why_glarus	9	33
144	102	102	json	[{"pk": 102, "model": "cms.placeholder", "fields": {"slot": "digitalglarus_why_glarus_beautiful_landscape", "default_width": null}}]	digitalglarus_why_glarus_beautiful_landscape	9	33
145	30	30	json	[{"pk": 30, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_build_a_tech_valley", "default_width": null}}]	digital_glarus_build_a_tech_valley	9	33
146	31	31	json	[{"pk": 31, "model": "cms.placeholder", "fields": {"slot": "digital_glarus_build_a_tech_valley_content", "default_width": null}}]	digital_glarus_build_a_tech_valley_content	9	33
147	5	5	json	[{"fields": {"title": "digital glarus home", "menu_title": "home", "language": "en-us", "meta_description": "", "redirect": "", "page": 5, "has_url_overwrite": true, "path": "digitalglarus", "creation_date": "2015-10-04T16:27:41.449Z", "page_title": "Digital Glarus", "slug": "digital-glarus-home", "published": true}, "model": "cms.title", "pk": 5}]	digital glarus home (digital-glarus-home, en-us)	16	34
148	5	5	json	[{"fields": {"changed_date": "2015-10-04T22:51:13.614Z", "publication_end_date": null, "parent": null, "site": 1, "revision_id": 0, "application_urls": "", "template": "cms/digitalglarus/index.html", "languages": "en-us", "soft_root": true, "path": "0005", "navigation_extenders": "", "login_required": false, "placeholders": [21, 22, 23, 24, 25, 26, 27, 28, 29], "application_namespace": null, "created_by": "ungleich", "depth": 1, "xframe_options": 0, "in_navigation": false, "publication_date": "2015-10-04T16:47:36.159Z", "reverse_id": null, "changed_by": "ungleich", "numchild": 2, "is_home": false, "creation_date": "2015-10-04T16:27:41.288Z", "limit_visibility_in_menu": null}, "model": "cms.page", "pk": 5}]	home	11	34
149	22	22	json	[{"fields": {"slot": "digital_glarus_build_a_tech_valley_content", "default_width": null}, "model": "cms.placeholder", "pk": 22}]	digital_glarus_build_a_tech_valley_content	9	34
150	23	23	json	[{"fields": {"slot": "digital_glarus_a_new_area", "default_width": null}, "model": "cms.placeholder", "pk": 23}]	digital_glarus_a_new_area	9	34
151	24	24	json	[{"fields": {"slot": "digital_glarus_a_new_area_content", "default_width": null}, "model": "cms.placeholder", "pk": 24}]	digital_glarus_a_new_area_content	9	34
152	25	25	json	[{"fields": {"slot": "digital_glarus_why_be_interested", "default_width": null}, "model": "cms.placeholder", "pk": 25}]	digital_glarus_why_be_interested	9	34
153	26	26	json	[{"fields": {"slot": "digital_glarus_why_be_interested_content", "default_width": null}, "model": "cms.placeholder", "pk": 26}]	digital_glarus_why_be_interested_content	9	34
154	27	27	json	[{"fields": {"slot": "digital_glarus_where_we_are", "default_width": null}, "model": "cms.placeholder", "pk": 27}]	digital_glarus_where_we_are	9	34
155	28	28	json	[{"fields": {"slot": "digital_glarus_where_we_are_content", "default_width": null}, "model": "cms.placeholder", "pk": 28}]	digital_glarus_where_we_are_content	9	34
156	29	29	json	[{"fields": {"slot": "digital_glarus_legend", "default_width": null}, "model": "cms.placeholder", "pk": 29}]	digital_glarus_legend	9	34
157	21	21	json	[{"fields": {"slot": "digital_glarus_build_a_tech_valley", "default_width": null}, "model": "cms.placeholder", "pk": 21}]	digital_glarus_build_a_tech_valley	9	34
158	5	5	json	[{"fields": {"title": "digital glarus home", "menu_title": "home", "language": "en-us", "meta_description": "", "redirect": "", "page": 5, "has_url_overwrite": true, "path": "digitalglarus", "creation_date": "2015-10-04T16:27:41.449Z", "page_title": "Digital Glarus", "slug": "digital-glarus-home", "published": true}, "model": "cms.title", "pk": 5}]	digital glarus home (digital-glarus-home, en-us)	16	35
159	5	5	json	[{"fields": {"changed_date": "2015-10-04T22:51:15.308Z", "publication_end_date": null, "parent": null, "site": 1, "revision_id": 0, "application_urls": "", "template": "cms/digitalglarus/index.html", "languages": "en-us", "soft_root": true, "path": "0005", "navigation_extenders": "", "login_required": false, "placeholders": [21, 22, 23, 24, 25, 26, 27, 28, 29], "application_namespace": null, "created_by": "ungleich", "depth": 1, "xframe_options": 0, "in_navigation": false, "publication_date": "2015-10-04T16:47:36.159Z", "reverse_id": null, "changed_by": "ungleich", "numchild": 2, "is_home": false, "creation_date": "2015-10-04T16:27:41.288Z", "limit_visibility_in_menu": null}, "model": "cms.page", "pk": 5}]	home	11	35
160	22	22	json	[{"fields": {"slot": "digital_glarus_build_a_tech_valley_content", "default_width": null}, "model": "cms.placeholder", "pk": 22}]	digital_glarus_build_a_tech_valley_content	9	35
161	23	23	json	[{"fields": {"slot": "digital_glarus_a_new_area", "default_width": null}, "model": "cms.placeholder", "pk": 23}]	digital_glarus_a_new_area	9	35
162	24	24	json	[{"fields": {"slot": "digital_glarus_a_new_area_content", "default_width": null}, "model": "cms.placeholder", "pk": 24}]	digital_glarus_a_new_area_content	9	35
163	25	25	json	[{"fields": {"slot": "digital_glarus_why_be_interested", "default_width": null}, "model": "cms.placeholder", "pk": 25}]	digital_glarus_why_be_interested	9	35
164	26	26	json	[{"fields": {"slot": "digital_glarus_why_be_interested_content", "default_width": null}, "model": "cms.placeholder", "pk": 26}]	digital_glarus_why_be_interested_content	9	35
165	27	27	json	[{"fields": {"slot": "digital_glarus_where_we_are", "default_width": null}, "model": "cms.placeholder", "pk": 27}]	digital_glarus_where_we_are	9	35
166	28	28	json	[{"fields": {"slot": "digital_glarus_where_we_are_content", "default_width": null}, "model": "cms.placeholder", "pk": 28}]	digital_glarus_where_we_are_content	9	35
167	29	29	json	[{"fields": {"slot": "digital_glarus_legend", "default_width": null}, "model": "cms.placeholder", "pk": 29}]	digital_glarus_legend	9	35
168	21	21	json	[{"fields": {"slot": "digital_glarus_build_a_tech_valley", "default_width": null}, "model": "cms.placeholder", "pk": 21}]	digital_glarus_build_a_tech_valley	9	35
169	5	5	json	[{"fields": {"title": "digital glarus home", "menu_title": "home", "language": "en-us", "meta_description": "", "redirect": "", "page": 5, "has_url_overwrite": true, "path": "digitalglarus", "creation_date": "2015-10-04T16:27:41.449Z", "page_title": "Digital Glarus", "slug": "digital-glarus-home", "published": true}, "model": "cms.title", "pk": 5}]	digital glarus home (digital-glarus-home, en-us)	16	36
170	5	5	json	[{"fields": {"changed_date": "2015-10-04T22:51:37.444Z", "publication_end_date": null, "parent": null, "site": 1, "revision_id": 0, "application_urls": "", "template": "cms/digitalglarus/index.html", "languages": "en-us", "soft_root": true, "path": "0005", "navigation_extenders": "", "login_required": false, "placeholders": [21, 22, 23, 24, 25, 26, 27, 28, 29], "application_namespace": null, "created_by": "ungleich", "depth": 1, "xframe_options": 0, "in_navigation": true, "publication_date": "2015-10-04T16:47:36.159Z", "reverse_id": null, "changed_by": "ungleich", "numchild": 2, "is_home": false, "creation_date": "2015-10-04T16:27:41.288Z", "limit_visibility_in_menu": null}, "model": "cms.page", "pk": 5}]	home	11	36
171	22	22	json	[{"fields": {"slot": "digital_glarus_build_a_tech_valley_content", "default_width": null}, "model": "cms.placeholder", "pk": 22}]	digital_glarus_build_a_tech_valley_content	9	36
172	23	23	json	[{"fields": {"slot": "digital_glarus_a_new_area", "default_width": null}, "model": "cms.placeholder", "pk": 23}]	digital_glarus_a_new_area	9	36
173	24	24	json	[{"fields": {"slot": "digital_glarus_a_new_area_content", "default_width": null}, "model": "cms.placeholder", "pk": 24}]	digital_glarus_a_new_area_content	9	36
174	25	25	json	[{"fields": {"slot": "digital_glarus_why_be_interested", "default_width": null}, "model": "cms.placeholder", "pk": 25}]	digital_glarus_why_be_interested	9	36
175	26	26	json	[{"fields": {"slot": "digital_glarus_why_be_interested_content", "default_width": null}, "model": "cms.placeholder", "pk": 26}]	digital_glarus_why_be_interested_content	9	36
176	27	27	json	[{"fields": {"slot": "digital_glarus_where_we_are", "default_width": null}, "model": "cms.placeholder", "pk": 27}]	digital_glarus_where_we_are	9	36
177	28	28	json	[{"fields": {"slot": "digital_glarus_where_we_are_content", "default_width": null}, "model": "cms.placeholder", "pk": 28}]	digital_glarus_where_we_are_content	9	36
178	29	29	json	[{"fields": {"slot": "digital_glarus_legend", "default_width": null}, "model": "cms.placeholder", "pk": 29}]	digital_glarus_legend	9	36
179	21	21	json	[{"fields": {"slot": "digital_glarus_build_a_tech_valley", "default_width": null}, "model": "cms.placeholder", "pk": 21}]	digital_glarus_build_a_tech_valley	9	36
180	3	3	json	[{"fields": {"title": "Blog", "menu_title": "Blog", "language": "en-us", "meta_description": "on OpenSource, technology, our passion and interests...", "redirect": "", "page": 3, "has_url_overwrite": false, "path": "", "creation_date": "2015-06-12T17:05:57.066Z", "page_title": "ungleich Blog", "slug": "blog", "published": true}, "model": "cms.title", "pk": 3}]	Blog (blog, en-us)	16	37
181	3	3	json	[{"fields": {"changed_date": "2015-10-04T22:53:00.281Z", "publication_end_date": null, "parent": null, "site": 1, "revision_id": 0, "application_urls": "BlogApp", "template": "cms/ungleichch/blog.html", "languages": "en-us", "soft_root": true, "path": "0003", "navigation_extenders": "", "login_required": false, "placeholders": [6], "application_namespace": "djangocms_blog", "created_by": "ungleich", "depth": 1, "xframe_options": 0, "in_navigation": true, "publication_date": "2015-06-12T17:17:49.261Z", "reverse_id": null, "changed_by": "ungleich", "numchild": 0, "is_home": true, "creation_date": "2015-06-12T17:05:57.028Z", "limit_visibility_in_menu": null}, "model": "cms.page", "pk": 3}]	Blog	11	37
182	6	6	json	[{"fields": {"slot": "page_content", "default_width": null}, "model": "cms.placeholder", "pk": 6}]	page_content	9	37
183	5	5	json	[{"fields": {"title": "digital glarus home", "menu_title": "home", "language": "en-us", "meta_description": "", "redirect": "", "page": 5, "has_url_overwrite": true, "path": "digitalglarus", "creation_date": "2015-10-04T16:27:41.449Z", "page_title": "Digital Glarus", "slug": "digital-glarus-home", "published": true}, "model": "cms.title", "pk": 5}]	digital glarus home (digital-glarus-home, en-us)	16	38
184	5	5	json	[{"fields": {"changed_date": "2015-10-04T22:55:29.682Z", "publication_end_date": null, "parent": null, "site": 1, "revision_id": 0, "application_urls": "", "template": "cms/digitalglarus/index.html", "languages": "en-us", "soft_root": false, "path": "0005", "navigation_extenders": "", "login_required": false, "placeholders": [21, 22, 23, 24, 25, 26, 27, 28, 29], "application_namespace": null, "created_by": "ungleich", "depth": 1, "xframe_options": 0, "in_navigation": true, "publication_date": "2015-10-04T16:47:36.159Z", "reverse_id": null, "changed_by": "ungleich", "numchild": 2, "is_home": false, "creation_date": "2015-10-04T16:27:41.288Z", "limit_visibility_in_menu": null}, "model": "cms.page", "pk": 5}]	home	11	38
185	22	22	json	[{"fields": {"slot": "digital_glarus_build_a_tech_valley_content", "default_width": null}, "model": "cms.placeholder", "pk": 22}]	digital_glarus_build_a_tech_valley_content	9	38
186	23	23	json	[{"fields": {"slot": "digital_glarus_a_new_area", "default_width": null}, "model": "cms.placeholder", "pk": 23}]	digital_glarus_a_new_area	9	38
187	24	24	json	[{"fields": {"slot": "digital_glarus_a_new_area_content", "default_width": null}, "model": "cms.placeholder", "pk": 24}]	digital_glarus_a_new_area_content	9	38
188	25	25	json	[{"fields": {"slot": "digital_glarus_why_be_interested", "default_width": null}, "model": "cms.placeholder", "pk": 25}]	digital_glarus_why_be_interested	9	38
189	26	26	json	[{"fields": {"slot": "digital_glarus_why_be_interested_content", "default_width": null}, "model": "cms.placeholder", "pk": 26}]	digital_glarus_why_be_interested_content	9	38
190	27	27	json	[{"fields": {"slot": "digital_glarus_where_we_are", "default_width": null}, "model": "cms.placeholder", "pk": 27}]	digital_glarus_where_we_are	9	38
191	28	28	json	[{"fields": {"slot": "digital_glarus_where_we_are_content", "default_width": null}, "model": "cms.placeholder", "pk": 28}]	digital_glarus_where_we_are_content	9	38
192	29	29	json	[{"fields": {"slot": "digital_glarus_legend", "default_width": null}, "model": "cms.placeholder", "pk": 29}]	digital_glarus_legend	9	38
193	21	21	json	[{"fields": {"slot": "digital_glarus_build_a_tech_valley", "default_width": null}, "model": "cms.placeholder", "pk": 21}]	digital_glarus_build_a_tech_valley	9	38
194	3	3	json	[{"fields": {"title": "Blog", "menu_title": "Blog", "language": "en-us", "meta_description": "on OpenSource, technology, our passion and interests...", "redirect": "", "page": 3, "has_url_overwrite": false, "path": "", "creation_date": "2015-06-12T17:05:57.066Z", "page_title": "ungleich Blog", "slug": "blog", "published": true}, "model": "cms.title", "pk": 3}]	Blog (blog, en-us)	16	39
195	3	3	json	[{"fields": {"changed_date": "2015-10-04T22:55:37.412Z", "publication_end_date": null, "parent": null, "site": 1, "revision_id": 0, "application_urls": "BlogApp", "template": "cms/ungleichch/blog.html", "languages": "en-us", "soft_root": false, "path": "0003", "navigation_extenders": "", "login_required": false, "placeholders": [6], "application_namespace": "djangocms_blog", "created_by": "ungleich", "depth": 1, "xframe_options": 0, "in_navigation": true, "publication_date": "2015-06-12T17:17:49.261Z", "reverse_id": null, "changed_by": "ungleich", "numchild": 0, "is_home": true, "creation_date": "2015-06-12T17:05:57.028Z", "limit_visibility_in_menu": null}, "model": "cms.page", "pk": 3}]	Blog	11	39
196	6	6	json	[{"fields": {"slot": "page_content", "default_width": null}, "model": "cms.placeholder", "pk": 6}]	page_content	9	39
197	5	5	json	[{"fields": {"title": "digital glarus home", "menu_title": "home", "language": "en-us", "meta_description": "", "redirect": "", "page": 5, "has_url_overwrite": true, "path": "digitalglarus", "creation_date": "2015-10-04T16:27:41.449Z", "page_title": "Digital Glarus", "slug": "digital-glarus-home", "published": true}, "model": "cms.title", "pk": 5}]	digital glarus home (digital-glarus-home, en-us)	16	40
198	5	5	json	[{"fields": {"changed_date": "2015-10-04T22:59:54.461Z", "publication_end_date": null, "parent": null, "site": 1, "revision_id": 0, "application_urls": "", "template": "cms/digitalglarus/index.html", "languages": "en-us", "soft_root": true, "path": "0005", "navigation_extenders": "", "login_required": false, "placeholders": [21, 22, 23, 24, 25, 26, 27, 28, 29], "application_namespace": null, "created_by": "ungleich", "depth": 1, "xframe_options": 0, "in_navigation": true, "publication_date": "2015-10-04T16:47:36.159Z", "reverse_id": null, "changed_by": "ungleich", "numchild": 2, "is_home": false, "creation_date": "2015-10-04T16:27:41.288Z", "limit_visibility_in_menu": null}, "model": "cms.page", "pk": 5}]	home	11	40
199	22	22	json	[{"fields": {"slot": "digital_glarus_build_a_tech_valley_content", "default_width": null}, "model": "cms.placeholder", "pk": 22}]	digital_glarus_build_a_tech_valley_content	9	40
200	23	23	json	[{"fields": {"slot": "digital_glarus_a_new_area", "default_width": null}, "model": "cms.placeholder", "pk": 23}]	digital_glarus_a_new_area	9	40
201	24	24	json	[{"fields": {"slot": "digital_glarus_a_new_area_content", "default_width": null}, "model": "cms.placeholder", "pk": 24}]	digital_glarus_a_new_area_content	9	40
202	25	25	json	[{"fields": {"slot": "digital_glarus_why_be_interested", "default_width": null}, "model": "cms.placeholder", "pk": 25}]	digital_glarus_why_be_interested	9	40
203	26	26	json	[{"fields": {"slot": "digital_glarus_why_be_interested_content", "default_width": null}, "model": "cms.placeholder", "pk": 26}]	digital_glarus_why_be_interested_content	9	40
204	27	27	json	[{"fields": {"slot": "digital_glarus_where_we_are", "default_width": null}, "model": "cms.placeholder", "pk": 27}]	digital_glarus_where_we_are	9	40
205	28	28	json	[{"fields": {"slot": "digital_glarus_where_we_are_content", "default_width": null}, "model": "cms.placeholder", "pk": 28}]	digital_glarus_where_we_are_content	9	40
206	29	29	json	[{"fields": {"slot": "digital_glarus_legend", "default_width": null}, "model": "cms.placeholder", "pk": 29}]	digital_glarus_legend	9	40
207	21	21	json	[{"fields": {"slot": "digital_glarus_build_a_tech_valley", "default_width": null}, "model": "cms.placeholder", "pk": 21}]	digital_glarus_build_a_tech_valley	9	40
208	11	11	json	[{"fields": {"menu_title": "blog", "path": "", "has_url_overwrite": false, "page": 3, "published": false, "title": "blog", "language": "de", "meta_description": "blog\\r\\n", "slug": "blog", "page_title": "blog", "creation_date": "2015-11-05T07:30:25.866Z", "redirect": null}, "pk": 11, "model": "cms.title"}]	blog (blog, de)	16	41
209	3	3	json	[{"fields": {"menu_title": "Blog", "path": "", "has_url_overwrite": false, "page": 3, "published": true, "title": "Blog", "language": "en-us", "meta_description": "on OpenSource, technology, our passion and interests...", "slug": "blog", "page_title": "ungleich Blog", "creation_date": "2015-06-12T17:05:57.066Z", "redirect": ""}, "pk": 3, "model": "cms.title"}]	Blog (blog, en-us)	16	41
210	3	3	json	[{"fields": {"path": "0003", "login_required": false, "created_by": "ungleich", "navigation_extenders": "", "languages": "en-us,de", "site": 1, "application_urls": "BlogApp", "application_namespace": "djangocms_blog", "in_navigation": true, "creation_date": "2015-06-12T17:05:57.028Z", "parent": null, "numchild": 0, "reverse_id": null, "xframe_options": 0, "revision_id": 0, "changed_by": "ungleich", "template": "cms/ungleichch/blog.html", "is_home": true, "depth": 1, "limit_visibility_in_menu": null, "publication_end_date": null, "publication_date": "2015-06-12T17:17:49.261Z", "soft_root": false, "placeholders": [6], "changed_date": "2015-11-05T07:34:36.974Z"}, "pk": 3, "model": "cms.page"}]	Blog	11	41
211	6	6	json	[{"fields": {"slot": "page_content", "default_width": null}, "pk": 6, "model": "cms.placeholder"}]	page_content	9	41
212	5	5	json	[{"pk": 5, "fields": {"in_navigation": true, "template": "cms/digitalglarus/index.html", "creation_date": "2015-10-04T16:27:41.288Z", "application_urls": "", "path": "0005", "application_namespace": null, "depth": 1, "xframe_options": 0, "publication_date": "2015-10-04T16:47:36.159Z", "languages": "en-us", "soft_root": true, "limit_visibility_in_menu": null, "parent": null, "revision_id": 0, "placeholders": [21, 22, 23, 24, 25, 26, 27, 28, 29, 112], "created_by": "ungleich", "is_home": false, "site": 1, "publication_end_date": null, "reverse_id": null, "numchild": 2, "changed_date": "2015-10-04T22:59:54.541Z", "changed_by": "ungleich", "navigation_extenders": "", "login_required": false}, "model": "cms.page"}]	home	11	42
213	76	76	json	[{"pk": 76, "fields": {"creation_date": "2016-02-08T09:37:50.103Z", "language": "en-us", "changed_date": "2016-02-08T09:37:50.214Z", "placeholder": 112, "path": "000L", "numchild": 0, "position": 0, "depth": 1, "parent": null, "plugin_type": "CMSGalleryPlugin"}, "model": "cms.cmsplugin"}]	76	10	42
214	112	112	json	[{"pk": 112, "fields": {"slot": "digital_glarus_gallery_grid", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_gallery_grid	9	42
215	21	21	json	[{"pk": 21, "fields": {"slot": "digital_glarus_build_a_tech_valley", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_build_a_tech_valley	9	42
216	22	22	json	[{"pk": 22, "fields": {"slot": "digital_glarus_build_a_tech_valley_content", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_build_a_tech_valley_content	9	42
217	23	23	json	[{"pk": 23, "fields": {"slot": "digital_glarus_a_new_area", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_a_new_area	9	42
218	24	24	json	[{"pk": 24, "fields": {"slot": "digital_glarus_a_new_area_content", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_a_new_area_content	9	42
219	25	25	json	[{"pk": 25, "fields": {"slot": "digital_glarus_why_be_interested", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_why_be_interested	9	42
220	26	26	json	[{"pk": 26, "fields": {"slot": "digital_glarus_why_be_interested_content", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_why_be_interested_content	9	42
221	27	27	json	[{"pk": 27, "fields": {"slot": "digital_glarus_where_we_are", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_where_we_are	9	42
222	28	28	json	[{"pk": 28, "fields": {"slot": "digital_glarus_where_we_are_content", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_where_we_are_content	9	42
223	29	29	json	[{"pk": 29, "fields": {"slot": "digital_glarus_legend", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_legend	9	42
224	5	5	json	[{"pk": 5, "fields": {"menu_title": "home", "creation_date": "2015-10-04T16:27:41.449Z", "page": 5, "slug": "digital-glarus-home", "redirect": "", "language": "en-us", "published": true, "meta_description": "", "page_title": "Digital Glarus", "path": "digitalglarus", "has_url_overwrite": true, "title": "digital glarus home"}, "model": "cms.title"}]	digital glarus home (digital-glarus-home, en-us)	16	42
225	5	5	json	[{"pk": 5, "fields": {"in_navigation": true, "template": "cms/digitalglarus/index.html", "creation_date": "2015-10-04T16:27:41.288Z", "application_urls": "", "path": "0005", "application_namespace": null, "depth": 1, "xframe_options": 0, "publication_date": "2015-10-04T16:47:36.159Z", "languages": "en-us", "soft_root": true, "limit_visibility_in_menu": null, "parent": null, "revision_id": 0, "placeholders": [21, 22, 23, 24, 25, 26, 27, 28, 29, 112], "created_by": "ungleich", "is_home": false, "site": 1, "publication_end_date": null, "reverse_id": null, "numchild": 2, "changed_date": "2016-02-08T09:37:50.339Z", "changed_by": "ungleich", "navigation_extenders": "", "login_required": false}, "model": "cms.page"}]	home	11	43
227	76	76	json	[{"pk": 76, "fields": {"creation_date": "2016-02-08T09:37:50.103Z", "language": "en-us", "changed_date": "2016-02-08T09:37:56.601Z", "placeholder": 112, "path": "000L", "numchild": 0, "position": 0, "depth": 1, "parent": null, "plugin_type": "CMSGalleryPlugin"}, "model": "cms.cmsplugin"}]	76	10	43
228	112	112	json	[{"pk": 112, "fields": {"slot": "digital_glarus_gallery_grid", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_gallery_grid	9	43
229	21	21	json	[{"pk": 21, "fields": {"slot": "digital_glarus_build_a_tech_valley", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_build_a_tech_valley	9	43
230	22	22	json	[{"pk": 22, "fields": {"slot": "digital_glarus_build_a_tech_valley_content", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_build_a_tech_valley_content	9	43
231	23	23	json	[{"pk": 23, "fields": {"slot": "digital_glarus_a_new_area", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_a_new_area	9	43
232	24	24	json	[{"pk": 24, "fields": {"slot": "digital_glarus_a_new_area_content", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_a_new_area_content	9	43
233	25	25	json	[{"pk": 25, "fields": {"slot": "digital_glarus_why_be_interested", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_why_be_interested	9	43
234	26	26	json	[{"pk": 26, "fields": {"slot": "digital_glarus_why_be_interested_content", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_why_be_interested_content	9	43
235	27	27	json	[{"pk": 27, "fields": {"slot": "digital_glarus_where_we_are", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_where_we_are	9	43
236	28	28	json	[{"pk": 28, "fields": {"slot": "digital_glarus_where_we_are_content", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_where_we_are_content	9	43
237	29	29	json	[{"pk": 29, "fields": {"slot": "digital_glarus_legend", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_legend	9	43
238	5	5	json	[{"pk": 5, "fields": {"menu_title": "home", "creation_date": "2015-10-04T16:27:41.449Z", "page": 5, "slug": "digital-glarus-home", "redirect": "", "language": "en-us", "published": true, "meta_description": "", "page_title": "Digital Glarus", "path": "digitalglarus", "has_url_overwrite": true, "title": "digital glarus home"}, "model": "cms.title"}]	digital glarus home (digital-glarus-home, en-us)	16	43
239	5	5	json	[{"pk": 5, "fields": {"in_navigation": true, "template": "cms/digitalglarus/index.html", "creation_date": "2015-10-04T16:27:41.288Z", "application_urls": "", "path": "0005", "application_namespace": null, "depth": 1, "xframe_options": 0, "publication_date": "2015-10-04T16:47:36.159Z", "languages": "en-us", "soft_root": true, "limit_visibility_in_menu": null, "parent": null, "revision_id": 0, "placeholders": [21, 22, 23, 24, 25, 26, 27, 28, 29, 112], "created_by": "ungleich", "is_home": false, "site": 1, "publication_end_date": null, "reverse_id": null, "numchild": 2, "changed_date": "2016-02-08T09:38:02.215Z", "changed_by": "ungleich", "navigation_extenders": "", "login_required": false}, "model": "cms.page"}]	home	11	44
240	76	76	json	[{"pk": 76, "fields": {"dgGallery": 1}, "model": "digitalglarus.dggalleryplugin"}]	76	65	44
241	76	76	json	[{"pk": 76, "fields": {"creation_date": "2016-02-08T09:37:50.103Z", "language": "en-us", "changed_date": "2016-02-08T09:37:56.601Z", "placeholder": 112, "path": "000L", "numchild": 0, "position": 0, "depth": 1, "parent": null, "plugin_type": "CMSGalleryPlugin"}, "model": "cms.cmsplugin"}]	76	10	44
242	112	112	json	[{"pk": 112, "fields": {"slot": "digital_glarus_gallery_grid", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_gallery_grid	9	44
243	21	21	json	[{"pk": 21, "fields": {"slot": "digital_glarus_build_a_tech_valley", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_build_a_tech_valley	9	44
244	22	22	json	[{"pk": 22, "fields": {"slot": "digital_glarus_build_a_tech_valley_content", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_build_a_tech_valley_content	9	44
245	23	23	json	[{"pk": 23, "fields": {"slot": "digital_glarus_a_new_area", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_a_new_area	9	44
246	24	24	json	[{"pk": 24, "fields": {"slot": "digital_glarus_a_new_area_content", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_a_new_area_content	9	44
247	25	25	json	[{"pk": 25, "fields": {"slot": "digital_glarus_why_be_interested", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_why_be_interested	9	44
248	26	26	json	[{"pk": 26, "fields": {"slot": "digital_glarus_why_be_interested_content", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_why_be_interested_content	9	44
249	27	27	json	[{"pk": 27, "fields": {"slot": "digital_glarus_where_we_are", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_where_we_are	9	44
250	28	28	json	[{"pk": 28, "fields": {"slot": "digital_glarus_where_we_are_content", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_where_we_are_content	9	44
251	29	29	json	[{"pk": 29, "fields": {"slot": "digital_glarus_legend", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_legend	9	44
252	5	5	json	[{"pk": 5, "fields": {"menu_title": "home", "creation_date": "2015-10-04T16:27:41.449Z", "page": 5, "slug": "digital-glarus-home", "redirect": "", "language": "en-us", "published": true, "meta_description": "", "page_title": "Digital Glarus", "path": "digitalglarus", "has_url_overwrite": true, "title": "digital glarus home"}, "model": "cms.title"}]	digital glarus home (digital-glarus-home, en-us)	16	44
253	113	113	json	[{"pk": 113, "fields": {"slot": "digitalglarus_why_glarus", "default_width": null}, "model": "cms.placeholder"}]	digitalglarus_why_glarus	9	45
254	114	114	json	[{"pk": 114, "fields": {"slot": "digitalglarus_why_glarus_beautiful_landscape", "default_width": null}, "model": "cms.placeholder"}]	digitalglarus_why_glarus_beautiful_landscape	9	45
255	115	115	json	[{"pk": 115, "fields": {"slot": "digitalglarus_why_glarus_affordable_price", "default_width": null}, "model": "cms.placeholder"}]	digitalglarus_why_glarus_affordable_price	9	45
256	116	116	json	[{"pk": 116, "fields": {"slot": "digitalglarus_why_glarus_direct_connection_zurich", "default_width": null}, "model": "cms.placeholder"}]	digitalglarus_why_glarus_direct_connection_zurich	9	45
257	117	117	json	[{"pk": 117, "fields": {"slot": "digital_glarus_legend", "default_width": null}, "model": "cms.placeholder"}]	digital_glarus_legend	9	45
258	12	12	json	[{"pk": 12, "fields": {"menu_title": "supporters", "creation_date": "2016-02-08T09:38:35.910Z", "page": 12, "slug": "supporters", "redirect": "", "language": "en-us", "published": true, "meta_description": "", "page_title": "supporters", "path": "supporters", "has_url_overwrite": false, "title": "supporters"}, "model": "cms.title"}]	supporters (supporters, en-us)	16	45
259	12	12	json	[{"pk": 12, "fields": {"in_navigation": true, "template": "INHERIT", "creation_date": "2016-02-08T09:38:35.737Z", "application_urls": "", "path": "0007", "application_namespace": null, "depth": 1, "xframe_options": 0, "publication_date": "2016-02-08T09:40:46.342Z", "languages": "en-us", "soft_root": false, "limit_visibility_in_menu": null, "parent": null, "revision_id": 0, "placeholders": [113, 114, 115, 116, 117], "created_by": "ungleich", "is_home": false, "site": 1, "publication_end_date": null, "reverse_id": null, "numchild": 0, "changed_date": "2016-02-08T09:40:46.453Z", "changed_by": "ungleich", "navigation_extenders": "", "login_required": false}, "model": "cms.page"}]	supporters	11	45
\.


--
-- Name: reversion_version_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('reversion_version_id_seq', 259, true);


--
-- Data for Name: taggit_tag; Type: TABLE DATA; Schema: public; Owner: app
--

COPY taggit_tag (id, name, slug) FROM stdin;
1	digitalglarus	digitalglarus
2	glarus	glarus
3	hosting	hosting
\.


--
-- Name: taggit_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('taggit_tag_id_seq', 3, true);


--
-- Data for Name: taggit_taggeditem; Type: TABLE DATA; Schema: public; Owner: app
--

COPY taggit_taggeditem (id, object_id, content_type_id, tag_id) FROM stdin;
5	11	53	1
7	10	53	1
16	12	53	3
\.


--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('taggit_taggeditem_id_seq', 16, true);


--
-- Data for Name: ungleich_ungleichpage; Type: TABLE DATA; Schema: public; Owner: app
--

COPY ungleich_ungleichpage (id, extended_object_id, public_extension_id, image_id) FROM stdin;
1	3	2	35
2	4	\N	35
\.


--
-- Name: ungleich_ungleichpage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('ungleich_ungleichpage_id_seq', 2, true);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: cms_aliaspluginmodel_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_aliaspluginmodel
    ADD CONSTRAINT cms_aliaspluginmodel_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cms_cmsplugin_path_6db4a772adcf443b_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmsplugin_path_6db4a772adcf443b_uniq UNIQUE (path);


--
-- Name: cms_cmsplugin_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmsplugin_pkey PRIMARY KEY (id);


--
-- Name: cms_globalpagepermission_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_globalpagepermission
    ADD CONSTRAINT cms_globalpagepermission_pkey PRIMARY KEY (id);


--
-- Name: cms_globalpagepermission_site_globalpagepermission_id_site__key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_globalpagepermission_sites
    ADD CONSTRAINT cms_globalpagepermission_site_globalpagepermission_id_site__key UNIQUE (globalpagepermission_id, site_id);


--
-- Name: cms_globalpagepermission_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_globalpagepermission_sites
    ADD CONSTRAINT cms_globalpagepermission_sites_pkey PRIMARY KEY (id);


--
-- Name: cms_page_path_b495adb731fe537_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_path_b495adb731fe537_uniq UNIQUE (path);


--
-- Name: cms_page_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_pkey PRIMARY KEY (id);


--
-- Name: cms_page_placeholders_page_id_placeholder_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page_placeholders
    ADD CONSTRAINT cms_page_placeholders_page_id_placeholder_id_key UNIQUE (page_id, placeholder_id);


--
-- Name: cms_page_placeholders_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page_placeholders
    ADD CONSTRAINT cms_page_placeholders_pkey PRIMARY KEY (id);


--
-- Name: cms_page_publisher_is_draft_603d95861eb3d85b_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_publisher_is_draft_603d95861eb3d85b_uniq UNIQUE (publisher_is_draft, site_id, application_namespace);


--
-- Name: cms_page_publisher_public_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_publisher_public_id_key UNIQUE (publisher_public_id);


--
-- Name: cms_page_reverse_id_38543d1ba5dbbf2f_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_reverse_id_38543d1ba5dbbf2f_uniq UNIQUE (reverse_id, site_id, publisher_is_draft);


--
-- Name: cms_pagepermission_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_pagepermission
    ADD CONSTRAINT cms_pagepermission_pkey PRIMARY KEY (id);


--
-- Name: cms_pageuser_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_pageuser
    ADD CONSTRAINT cms_pageuser_pkey PRIMARY KEY (user_ptr_id);


--
-- Name: cms_pageusergroup_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_pageusergroup
    ADD CONSTRAINT cms_pageusergroup_pkey PRIMARY KEY (group_ptr_id);


--
-- Name: cms_placeholder_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_placeholder
    ADD CONSTRAINT cms_placeholder_pkey PRIMARY KEY (id);


--
-- Name: cms_placeholderreference_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_placeholderreference
    ADD CONSTRAINT cms_placeholderreference_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cms_staticplaceholder_code_13295693baa76e9c_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplaceholder_code_13295693baa76e9c_uniq UNIQUE (code, site_id);


--
-- Name: cms_staticplaceholder_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplaceholder_pkey PRIMARY KEY (id);


--
-- Name: cms_title_language_6c0f5d7214ca8030_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_language_6c0f5d7214ca8030_uniq UNIQUE (language, page_id);


--
-- Name: cms_title_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_pkey PRIMARY KEY (id);


--
-- Name: cms_title_publisher_public_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_publisher_public_id_key UNIQUE (publisher_public_id);


--
-- Name: cms_usersettings_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_usersettings
    ADD CONSTRAINT cms_usersettings_pkey PRIMARY KEY (id);


--
-- Name: cms_usersettings_user_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_usersettings
    ADD CONSTRAINT cms_usersettings_user_id_key UNIQUE (user_id);


--
-- Name: cmsplugin_filer_file_filerfile_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_file_filerfile
    ADD CONSTRAINT cmsplugin_filer_file_filerfile_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cmsplugin_filer_folder_filerfolder_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_folder_filerfolder
    ADD CONSTRAINT cmsplugin_filer_folder_filerfolder_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cmsplugin_filer_image_filerimage_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_image_filerimage
    ADD CONSTRAINT cmsplugin_filer_image_filerimage_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cmsplugin_filer_image_thumbnailoption_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_image_thumbnailoption
    ADD CONSTRAINT cmsplugin_filer_image_thumbnailoption_pkey PRIMARY KEY (id);


--
-- Name: cmsplugin_filer_link_filerlinkplugin_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_link_filerlinkplugin
    ADD CONSTRAINT cmsplugin_filer_link_filerlinkplugin_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cmsplugin_filer_teaser_filerteaser_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_teaser_filerteaser
    ADD CONSTRAINT cmsplugin_filer_teaser_filerteaser_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cmsplugin_filer_video_filervideo_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_video_filervideo
    ADD CONSTRAINT cmsplugin_filer_video_filervideo_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: digitalglarus_dggallery_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY digitalglarus_dggallery
    ADD CONSTRAINT digitalglarus_dggallery_pkey PRIMARY KEY (id);


--
-- Name: digitalglarus_dggalleryplugin_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY digitalglarus_dggalleryplugin
    ADD CONSTRAINT digitalglarus_dggalleryplugin_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: digitalglarus_dgpicture_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY digitalglarus_dgpicture
    ADD CONSTRAINT digitalglarus_dgpicture_pkey PRIMARY KEY (id);


--
-- Name: digitalglarus_dgsupportersplugin_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY digitalglarus_dgsupportersplugin
    ADD CONSTRAINT digitalglarus_dgsupportersplugin_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: digitalglarus_message_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY digitalglarus_message
    ADD CONSTRAINT digitalglarus_message_pkey PRIMARY KEY (id);


--
-- Name: digitalglarus_supporter_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY digitalglarus_supporter
    ADD CONSTRAINT digitalglarus_supporter_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_3dcea89a55f2eebc_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_3dcea89a55f2eebc_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_select2_keymap_key_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_select2_keymap
    ADD CONSTRAINT django_select2_keymap_key_key UNIQUE (key);


--
-- Name: django_select2_keymap_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_select2_keymap
    ADD CONSTRAINT django_select2_keymap_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_authorentriesp_authorentriesplugin_id_user_i_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin_authors
    ADD CONSTRAINT djangocms_blog_authorentriesp_authorentriesplugin_id_user_i_key UNIQUE (authorentriesplugin_id, user_id);


--
-- Name: djangocms_blog_authorentriesplugin_authors_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin_authors
    ADD CONSTRAINT djangocms_blog_authorentriesplugin_authors_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_authorentriesplugin_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin
    ADD CONSTRAINT djangocms_blog_authorentriesplugin_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_blog_blogcategory__language_code_a19aa8b8cfb0d53_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_blogcategory_translation
    ADD CONSTRAINT djangocms_blog_blogcategory__language_code_a19aa8b8cfb0d53_uniq UNIQUE (language_code, slug);


--
-- Name: djangocms_blog_blogcategory_language_code_755572fed22105af_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_blogcategory_translation
    ADD CONSTRAINT djangocms_blog_blogcategory_language_code_755572fed22105af_uniq UNIQUE (language_code, master_id);


--
-- Name: djangocms_blog_blogcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_blogcategory
    ADD CONSTRAINT djangocms_blog_blogcategory_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_blogcategory_translation_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_blogcategory_translation
    ADD CONSTRAINT djangocms_blog_blogcategory_translation_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_latestpostsplu_latestpostsplugin_id_blogcate_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_categories
    ADD CONSTRAINT djangocms_blog_latestpostsplu_latestpostsplugin_id_blogcate_key UNIQUE (latestpostsplugin_id, blogcategory_id);


--
-- Name: djangocms_blog_latestpostsplugi_latestpostsplugin_id_tag_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_tags
    ADD CONSTRAINT djangocms_blog_latestpostsplugi_latestpostsplugin_id_tag_id_key UNIQUE (latestpostsplugin_id, tag_id);


--
-- Name: djangocms_blog_latestpostsplugin_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_categories
    ADD CONSTRAINT djangocms_blog_latestpostsplugin_categories_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_latestpostsplugin_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin
    ADD CONSTRAINT djangocms_blog_latestpostsplugin_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_blog_latestpostsplugin_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_tags
    ADD CONSTRAINT djangocms_blog_latestpostsplugin_tags_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_post_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_categories
    ADD CONSTRAINT djangocms_blog_post_categories_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_post_categories_post_id_blogcategory_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_categories
    ADD CONSTRAINT djangocms_blog_post_categories_post_id_blogcategory_id_key UNIQUE (post_id, blogcategory_id);


--
-- Name: djangocms_blog_post_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post
    ADD CONSTRAINT djangocms_blog_post_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_post_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_sites
    ADD CONSTRAINT djangocms_blog_post_sites_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_post_sites_post_id_site_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_sites
    ADD CONSTRAINT djangocms_blog_post_sites_post_id_site_id_key UNIQUE (post_id, site_id);


--
-- Name: djangocms_blog_post_transla_language_code_38d8970fc71783dd_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_translation
    ADD CONSTRAINT djangocms_blog_post_transla_language_code_38d8970fc71783dd_uniq UNIQUE (language_code, slug);


--
-- Name: djangocms_blog_post_transla_language_code_727992a8ca095c7f_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_translation
    ADD CONSTRAINT djangocms_blog_post_transla_language_code_727992a8ca095c7f_uniq UNIQUE (language_code, master_id);


--
-- Name: djangocms_blog_post_translation_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_translation
    ADD CONSTRAINT djangocms_blog_post_translation_pkey PRIMARY KEY (id);


--
-- Name: djangocms_flash_flash_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_flash_flash
    ADD CONSTRAINT djangocms_flash_flash_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_googlemap_googlemap_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_googlemap_googlemap
    ADD CONSTRAINT djangocms_googlemap_googlemap_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_inherit_inheritpageplaceholder_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_inherit_inheritpageplaceholder
    ADD CONSTRAINT djangocms_inherit_inheritpageplaceholder_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_link_link_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_link_link
    ADD CONSTRAINT djangocms_link_link_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_page_meta_pagemeta_extended_object_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_page_meta_pagemeta
    ADD CONSTRAINT djangocms_page_meta_pagemeta_extended_object_id_key UNIQUE (extended_object_id);


--
-- Name: djangocms_page_meta_pagemeta_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_page_meta_pagemeta
    ADD CONSTRAINT djangocms_page_meta_pagemeta_pkey PRIMARY KEY (id);


--
-- Name: djangocms_page_meta_pagemeta_public_extension_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_page_meta_pagemeta
    ADD CONSTRAINT djangocms_page_meta_pagemeta_public_extension_id_key UNIQUE (public_extension_id);


--
-- Name: djangocms_page_meta_titlemeta_extended_object_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_page_meta_titlemeta
    ADD CONSTRAINT djangocms_page_meta_titlemeta_extended_object_id_key UNIQUE (extended_object_id);


--
-- Name: djangocms_page_meta_titlemeta_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_page_meta_titlemeta
    ADD CONSTRAINT djangocms_page_meta_titlemeta_pkey PRIMARY KEY (id);


--
-- Name: djangocms_page_meta_titlemeta_public_extension_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_page_meta_titlemeta
    ADD CONSTRAINT djangocms_page_meta_titlemeta_public_extension_id_key UNIQUE (public_extension_id);


--
-- Name: djangocms_snippet_snippet_name_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_snippet_snippet
    ADD CONSTRAINT djangocms_snippet_snippet_name_key UNIQUE (name);


--
-- Name: djangocms_snippet_snippet_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_snippet_snippet
    ADD CONSTRAINT djangocms_snippet_snippet_pkey PRIMARY KEY (id);


--
-- Name: djangocms_snippet_snippetptr_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_snippet_snippetptr
    ADD CONSTRAINT djangocms_snippet_snippetptr_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_teaser_teaser_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_teaser_teaser
    ADD CONSTRAINT djangocms_teaser_teaser_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_text_ckeditor_text_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_text_ckeditor_text
    ADD CONSTRAINT djangocms_text_ckeditor_text_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: easy_thumbnails_source_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY easy_thumbnails_source
    ADD CONSTRAINT easy_thumbnails_source_pkey PRIMARY KEY (id);


--
-- Name: easy_thumbnails_source_storage_hash_7c8eb4f6f9dd654b_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY easy_thumbnails_source
    ADD CONSTRAINT easy_thumbnails_source_storage_hash_7c8eb4f6f9dd654b_uniq UNIQUE (storage_hash, name);


--
-- Name: easy_thumbnails_thumbnail_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY easy_thumbnails_thumbnail
    ADD CONSTRAINT easy_thumbnails_thumbnail_pkey PRIMARY KEY (id);


--
-- Name: easy_thumbnails_thumbnail_storage_hash_7fddac563f20b9d1_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY easy_thumbnails_thumbnail
    ADD CONSTRAINT easy_thumbnails_thumbnail_storage_hash_7fddac563f20b9d1_uniq UNIQUE (storage_hash, name, source_id);


--
-- Name: easy_thumbnails_thumbnaildimensions_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY easy_thumbnails_thumbnaildimensions
    ADD CONSTRAINT easy_thumbnails_thumbnaildimensions_pkey PRIMARY KEY (id);


--
-- Name: easy_thumbnails_thumbnaildimensions_thumbnail_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY easy_thumbnails_thumbnaildimensions
    ADD CONSTRAINT easy_thumbnails_thumbnaildimensions_thumbnail_id_key UNIQUE (thumbnail_id);


--
-- Name: filer_clipboard_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_clipboard
    ADD CONSTRAINT filer_clipboard_pkey PRIMARY KEY (id);


--
-- Name: filer_clipboarditem_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_clipboarditem
    ADD CONSTRAINT filer_clipboarditem_pkey PRIMARY KEY (id);


--
-- Name: filer_file_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_file
    ADD CONSTRAINT filer_file_pkey PRIMARY KEY (id);


--
-- Name: filer_folder_parent_id_1390b0846a51c444_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_folder
    ADD CONSTRAINT filer_folder_parent_id_1390b0846a51c444_uniq UNIQUE (parent_id, name);


--
-- Name: filer_folder_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_folder
    ADD CONSTRAINT filer_folder_pkey PRIMARY KEY (id);


--
-- Name: filer_folderpermission_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_folderpermission
    ADD CONSTRAINT filer_folderpermission_pkey PRIMARY KEY (id);


--
-- Name: filer_image_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_image
    ADD CONSTRAINT filer_image_pkey PRIMARY KEY (file_ptr_id);


--
-- Name: hosting_railsbetauser_email_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY hosting_railsbetauser
    ADD CONSTRAINT hosting_railsbetauser_email_key UNIQUE (email);


--
-- Name: hosting_railsbetauser_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY hosting_railsbetauser
    ADD CONSTRAINT hosting_railsbetauser_pkey PRIMARY KEY (id);


--
-- Name: menus_cachekey_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY menus_cachekey
    ADD CONSTRAINT menus_cachekey_pkey PRIMARY KEY (id);


--
-- Name: railshosting_railsbetauser_email_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY railshosting_railsbetauser
    ADD CONSTRAINT railshosting_railsbetauser_email_key UNIQUE (email);


--
-- Name: railshosting_railsbetauser_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY railshosting_railsbetauser
    ADD CONSTRAINT railshosting_railsbetauser_pkey PRIMARY KEY (id);


--
-- Name: reversion_revision_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY reversion_revision
    ADD CONSTRAINT reversion_revision_pkey PRIMARY KEY (id);


--
-- Name: reversion_version_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY reversion_version
    ADD CONSTRAINT reversion_version_pkey PRIMARY KEY (id);


--
-- Name: taggit_tag_name_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_name_key UNIQUE (name);


--
-- Name: taggit_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_pkey PRIMARY KEY (id);


--
-- Name: taggit_tag_slug_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_slug_key UNIQUE (slug);


--
-- Name: taggit_taggeditem_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_pkey PRIMARY KEY (id);


--
-- Name: ungleich_ungleichpage_extended_object_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY ungleich_ungleichpage
    ADD CONSTRAINT ungleich_ungleichpage_extended_object_id_key UNIQUE (extended_object_id);


--
-- Name: ungleich_ungleichpage_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY ungleich_ungleichpage
    ADD CONSTRAINT ungleich_ungleichpage_pkey PRIMARY KEY (id);


--
-- Name: ungleich_ungleichpage_public_extension_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY ungleich_ungleichpage
    ADD CONSTRAINT ungleich_ungleichpage_public_extension_id_key UNIQUE (public_extension_id);


--
-- Name: auth_group_name_278a4cf7a334bf0c_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_group_name_278a4cf7a334bf0c_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_186bc59fbaa414d5_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_user_username_186bc59fbaa414d5_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: cms_aliaspluginmodel_921abf5c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_aliaspluginmodel_921abf5c ON cms_aliaspluginmodel USING btree (alias_placeholder_id);


--
-- Name: cms_aliaspluginmodel_b25eaab4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_aliaspluginmodel_b25eaab4 ON cms_aliaspluginmodel USING btree (plugin_id);


--
-- Name: cms_cmsplugin_667a6151; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_cmsplugin_667a6151 ON cms_cmsplugin USING btree (placeholder_id);


--
-- Name: cms_cmsplugin_6be37982; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_cmsplugin_6be37982 ON cms_cmsplugin USING btree (parent_id);


--
-- Name: cms_cmsplugin_8512ae7d; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_cmsplugin_8512ae7d ON cms_cmsplugin USING btree (language);


--
-- Name: cms_cmsplugin_b5e4cf8f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_cmsplugin_b5e4cf8f ON cms_cmsplugin USING btree (plugin_type);


--
-- Name: cms_cmsplugin_language_7123ba4ab8692cf5_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_cmsplugin_language_7123ba4ab8692cf5_like ON cms_cmsplugin USING btree (language varchar_pattern_ops);


--
-- Name: cms_cmsplugin_plugin_type_4ab9d6bfbdea06a4_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_cmsplugin_plugin_type_4ab9d6bfbdea06a4_like ON cms_cmsplugin USING btree (plugin_type varchar_pattern_ops);


--
-- Name: cms_globalpagepermission_0e939a4f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_globalpagepermission_0e939a4f ON cms_globalpagepermission USING btree (group_id);


--
-- Name: cms_globalpagepermission_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_globalpagepermission_e8701ad4 ON cms_globalpagepermission USING btree (user_id);


--
-- Name: cms_globalpagepermission_sites_9365d6e7; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_globalpagepermission_sites_9365d6e7 ON cms_globalpagepermission_sites USING btree (site_id);


--
-- Name: cms_globalpagepermission_sites_a3d12ecd; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_globalpagepermission_sites_a3d12ecd ON cms_globalpagepermission_sites USING btree (globalpagepermission_id);


--
-- Name: cms_page_1d85575d; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_1d85575d ON cms_page USING btree (soft_root);


--
-- Name: cms_page_2247c5f0; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_2247c5f0 ON cms_page USING btree (publication_end_date);


--
-- Name: cms_page_3d9ef52f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_3d9ef52f ON cms_page USING btree (reverse_id);


--
-- Name: cms_page_4fa1c803; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_4fa1c803 ON cms_page USING btree (is_home);


--
-- Name: cms_page_6be37982; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_6be37982 ON cms_page USING btree (parent_id);


--
-- Name: cms_page_7b8acfa6; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_7b8acfa6 ON cms_page USING btree (navigation_extenders);


--
-- Name: cms_page_9365d6e7; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_9365d6e7 ON cms_page USING btree (site_id);


--
-- Name: cms_page_93b83098; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_93b83098 ON cms_page USING btree (publication_date);


--
-- Name: cms_page_application_urls_71bd190d025877b8_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_application_urls_71bd190d025877b8_like ON cms_page USING btree (application_urls varchar_pattern_ops);


--
-- Name: cms_page_b7700099; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_b7700099 ON cms_page USING btree (publisher_is_draft);


--
-- Name: cms_page_cb540373; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_cb540373 ON cms_page USING btree (limit_visibility_in_menu);


--
-- Name: cms_page_db3eb53f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_db3eb53f ON cms_page USING btree (in_navigation);


--
-- Name: cms_page_e721871e; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_e721871e ON cms_page USING btree (application_urls);


--
-- Name: cms_page_navigation_extenders_3bf544ece0950dc2_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_navigation_extenders_3bf544ece0950dc2_like ON cms_page USING btree (navigation_extenders varchar_pattern_ops);


--
-- Name: cms_page_placeholders_1a63c800; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_placeholders_1a63c800 ON cms_page_placeholders USING btree (page_id);


--
-- Name: cms_page_placeholders_667a6151; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_placeholders_667a6151 ON cms_page_placeholders USING btree (placeholder_id);


--
-- Name: cms_page_reverse_id_66ad1d01e5dfa704_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_reverse_id_66ad1d01e5dfa704_like ON cms_page USING btree (reverse_id varchar_pattern_ops);


--
-- Name: cms_pagepermission_0e939a4f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_pagepermission_0e939a4f ON cms_pagepermission USING btree (group_id);


--
-- Name: cms_pagepermission_1a63c800; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_pagepermission_1a63c800 ON cms_pagepermission USING btree (page_id);


--
-- Name: cms_pagepermission_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_pagepermission_e8701ad4 ON cms_pagepermission USING btree (user_id);


--
-- Name: cms_pageuser_e93cb7eb; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_pageuser_e93cb7eb ON cms_pageuser USING btree (created_by_id);


--
-- Name: cms_pageusergroup_e93cb7eb; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_pageusergroup_e93cb7eb ON cms_pageusergroup USING btree (created_by_id);


--
-- Name: cms_placeholder_5e97994e; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_placeholder_5e97994e ON cms_placeholder USING btree (slot);


--
-- Name: cms_placeholder_slot_5cc23865c802b1e2_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_placeholder_slot_5cc23865c802b1e2_like ON cms_placeholder USING btree (slot varchar_pattern_ops);


--
-- Name: cms_placeholderreference_328d0afc; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_placeholderreference_328d0afc ON cms_placeholderreference USING btree (placeholder_ref_id);


--
-- Name: cms_staticplaceholder_1ee2744d; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_staticplaceholder_1ee2744d ON cms_staticplaceholder USING btree (public_id);


--
-- Name: cms_staticplaceholder_5cb48773; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_staticplaceholder_5cb48773 ON cms_staticplaceholder USING btree (draft_id);


--
-- Name: cms_staticplaceholder_9365d6e7; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_staticplaceholder_9365d6e7 ON cms_staticplaceholder USING btree (site_id);


--
-- Name: cms_title_1268de9a; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_1268de9a ON cms_title USING btree (has_url_overwrite);


--
-- Name: cms_title_1a63c800; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_1a63c800 ON cms_title USING btree (page_id);


--
-- Name: cms_title_2dbcba41; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_2dbcba41 ON cms_title USING btree (slug);


--
-- Name: cms_title_8512ae7d; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_8512ae7d ON cms_title USING btree (language);


--
-- Name: cms_title_b7700099; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_b7700099 ON cms_title USING btree (publisher_is_draft);


--
-- Name: cms_title_d6fe1d0b; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_d6fe1d0b ON cms_title USING btree (path);


--
-- Name: cms_title_f7202fc0; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_f7202fc0 ON cms_title USING btree (publisher_state);


--
-- Name: cms_title_language_4a0d9e2ff2ad085c_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_language_4a0d9e2ff2ad085c_like ON cms_title USING btree (language varchar_pattern_ops);


--
-- Name: cms_title_path_631a79107e3c59a2_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_path_631a79107e3c59a2_like ON cms_title USING btree (path varchar_pattern_ops);


--
-- Name: cms_title_slug_1a7da21be398730e_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_slug_1a7da21be398730e_like ON cms_title USING btree (slug varchar_pattern_ops);


--
-- Name: cms_usersettings_2655b062; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_usersettings_2655b062 ON cms_usersettings USING btree (clipboard_id);


--
-- Name: cmsplugin_filer_file_filerfile_814552b9; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_file_filerfile_814552b9 ON cmsplugin_filer_file_filerfile USING btree (file_id);


--
-- Name: cmsplugin_filer_folder_filerfolder_a8a44dbb; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_folder_filerfolder_a8a44dbb ON cmsplugin_filer_folder_filerfolder USING btree (folder_id);


--
-- Name: cmsplugin_filer_image_filerimage_0fe0fc57; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_image_filerimage_0fe0fc57 ON cmsplugin_filer_image_filerimage USING btree (file_link_id);


--
-- Name: cmsplugin_filer_image_filerimage_6b85b7b1; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_image_filerimage_6b85b7b1 ON cmsplugin_filer_image_filerimage USING btree (thumbnail_option_id);


--
-- Name: cmsplugin_filer_image_filerimage_d916d256; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_image_filerimage_d916d256 ON cmsplugin_filer_image_filerimage USING btree (page_link_id);


--
-- Name: cmsplugin_filer_image_filerimage_f33175e6; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_image_filerimage_f33175e6 ON cmsplugin_filer_image_filerimage USING btree (image_id);


--
-- Name: cmsplugin_filer_link_filerlinkplugin_814552b9; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_link_filerlinkplugin_814552b9 ON cmsplugin_filer_link_filerlinkplugin USING btree (file_id);


--
-- Name: cmsplugin_filer_link_filerlinkplugin_d916d256; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_link_filerlinkplugin_d916d256 ON cmsplugin_filer_link_filerlinkplugin USING btree (page_link_id);


--
-- Name: cmsplugin_filer_teaser_filerteaser_d916d256; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_teaser_filerteaser_d916d256 ON cmsplugin_filer_teaser_filerteaser USING btree (page_link_id);


--
-- Name: cmsplugin_filer_teaser_filerteaser_f33175e6; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_teaser_filerteaser_f33175e6 ON cmsplugin_filer_teaser_filerteaser USING btree (image_id);


--
-- Name: cmsplugin_filer_video_filervideo_d1b173c8; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_video_filervideo_d1b173c8 ON cmsplugin_filer_video_filervideo USING btree (movie_id);


--
-- Name: cmsplugin_filer_video_filervideo_f33175e6; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_video_filervideo_f33175e6 ON cmsplugin_filer_video_filervideo USING btree (image_id);


--
-- Name: digitalglarus_dggallery_6be37982; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX digitalglarus_dggallery_6be37982 ON digitalglarus_dggallery USING btree (parent_id);


--
-- Name: digitalglarus_dggalleryplugin_6cc1e242; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX digitalglarus_dggalleryplugin_6cc1e242 ON digitalglarus_dggalleryplugin USING btree ("dgGallery_id");


--
-- Name: digitalglarus_dgpicture_6d994cdb; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX digitalglarus_dgpicture_6d994cdb ON digitalglarus_dgpicture USING btree (gallery_id);


--
-- Name: digitalglarus_dgpicture_f33175e6; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX digitalglarus_dgpicture_f33175e6 ON digitalglarus_dgpicture USING btree (image_id);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_select2_keymap_key_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX django_select2_keymap_key_like ON django_select2_keymap USING btree (key varchar_pattern_ops);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_61253c6c71e29745_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX django_session_session_key_61253c6c71e29745_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: djangocms_blog_authorentriesplugin_authors_793c8338; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_authorentriesplugin_authors_793c8338 ON djangocms_blog_authorentriesplugin_authors USING btree (authorentriesplugin_id);


--
-- Name: djangocms_blog_authorentriesplugin_authors_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_authorentriesplugin_authors_e8701ad4 ON djangocms_blog_authorentriesplugin_authors USING btree (user_id);


--
-- Name: djangocms_blog_blogcategory_6be37982; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_blogcategory_6be37982 ON djangocms_blog_blogcategory USING btree (parent_id);


--
-- Name: djangocms_blog_blogcategory_language_code_6d38c82aaa83570a_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_blogcategory_language_code_6d38c82aaa83570a_like ON djangocms_blog_blogcategory_translation USING btree (language_code varchar_pattern_ops);


--
-- Name: djangocms_blog_blogcategory_translat_slug_6e348a9ab9a538a7_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_blogcategory_translat_slug_6e348a9ab9a538a7_like ON djangocms_blog_blogcategory_translation USING btree (slug varchar_pattern_ops);


--
-- Name: djangocms_blog_blogcategory_translation_2dbcba41; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_blogcategory_translation_2dbcba41 ON djangocms_blog_blogcategory_translation USING btree (slug);


--
-- Name: djangocms_blog_blogcategory_translation_60716c2f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_blogcategory_translation_60716c2f ON djangocms_blog_blogcategory_translation USING btree (language_code);


--
-- Name: djangocms_blog_blogcategory_translation_90349b61; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_blogcategory_translation_90349b61 ON djangocms_blog_blogcategory_translation USING btree (master_id);


--
-- Name: djangocms_blog_latestpostsplugin_categories_efb54956; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_latestpostsplugin_categories_efb54956 ON djangocms_blog_latestpostsplugin_categories USING btree (blogcategory_id);


--
-- Name: djangocms_blog_latestpostsplugin_categories_fda89e10; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_latestpostsplugin_categories_fda89e10 ON djangocms_blog_latestpostsplugin_categories USING btree (latestpostsplugin_id);


--
-- Name: djangocms_blog_latestpostsplugin_tags_76f094bc; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_latestpostsplugin_tags_76f094bc ON djangocms_blog_latestpostsplugin_tags USING btree (tag_id);


--
-- Name: djangocms_blog_latestpostsplugin_tags_fda89e10; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_latestpostsplugin_tags_fda89e10 ON djangocms_blog_latestpostsplugin_tags USING btree (latestpostsplugin_id);


--
-- Name: djangocms_blog_post_36b62cbe; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_36b62cbe ON djangocms_blog_post USING btree (main_image_id);


--
-- Name: djangocms_blog_post_4f331e2f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_4f331e2f ON djangocms_blog_post USING btree (author_id);


--
-- Name: djangocms_blog_post_53808359; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_53808359 ON djangocms_blog_post USING btree (main_image_full_id);


--
-- Name: djangocms_blog_post_9d0a35cc; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_9d0a35cc ON djangocms_blog_post USING btree (main_image_thumbnail_id);


--
-- Name: djangocms_blog_post_categories_efb54956; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_categories_efb54956 ON djangocms_blog_post_categories USING btree (blogcategory_id);


--
-- Name: djangocms_blog_post_categories_f3aa1999; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_categories_f3aa1999 ON djangocms_blog_post_categories USING btree (post_id);


--
-- Name: djangocms_blog_post_e14f02ad; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_e14f02ad ON djangocms_blog_post USING btree (content_id);


--
-- Name: djangocms_blog_post_sites_9365d6e7; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_sites_9365d6e7 ON djangocms_blog_post_sites USING btree (site_id);


--
-- Name: djangocms_blog_post_sites_f3aa1999; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_sites_f3aa1999 ON djangocms_blog_post_sites USING btree (post_id);


--
-- Name: djangocms_blog_post_transla_language_code_7ce952443f776c26_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_transla_language_code_7ce952443f776c26_like ON djangocms_blog_post_translation USING btree (language_code varchar_pattern_ops);


--
-- Name: djangocms_blog_post_translation_2dbcba41; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_translation_2dbcba41 ON djangocms_blog_post_translation USING btree (slug);


--
-- Name: djangocms_blog_post_translation_60716c2f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_translation_60716c2f ON djangocms_blog_post_translation USING btree (language_code);


--
-- Name: djangocms_blog_post_translation_90349b61; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_translation_90349b61 ON djangocms_blog_post_translation USING btree (master_id);


--
-- Name: djangocms_blog_post_translation_slug_5a481371b5483e29_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_translation_slug_5a481371b5483e29_like ON djangocms_blog_post_translation USING btree (slug varchar_pattern_ops);


--
-- Name: djangocms_inherit_inheritpageplaceholder_ccbb37bf; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_inherit_inheritpageplaceholder_ccbb37bf ON djangocms_inherit_inheritpageplaceholder USING btree (from_page_id);


--
-- Name: djangocms_link_link_d916d256; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_link_link_d916d256 ON djangocms_link_link USING btree (page_link_id);


--
-- Name: djangocms_page_meta_pagemeta_f149115b; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_page_meta_pagemeta_f149115b ON djangocms_page_meta_pagemeta USING btree (og_author_id);


--
-- Name: djangocms_page_meta_pagemeta_f33175e6; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_page_meta_pagemeta_f33175e6 ON djangocms_page_meta_pagemeta USING btree (image_id);


--
-- Name: djangocms_page_meta_titlemeta_f33175e6; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_page_meta_titlemeta_f33175e6 ON djangocms_page_meta_titlemeta USING btree (image_id);


--
-- Name: djangocms_snippet_snippet_name_2d01e17f7fe649fb_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_snippet_snippet_name_2d01e17f7fe649fb_like ON djangocms_snippet_snippet USING btree (name varchar_pattern_ops);


--
-- Name: djangocms_snippet_snippetptr_cfd011c9; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_snippet_snippetptr_cfd011c9 ON djangocms_snippet_snippetptr USING btree (snippet_id);


--
-- Name: djangocms_teaser_teaser_d916d256; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_teaser_teaser_d916d256 ON djangocms_teaser_teaser USING btree (page_link_id);


--
-- Name: easy_thumbnails_source_b068931c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_source_b068931c ON easy_thumbnails_source USING btree (name);


--
-- Name: easy_thumbnails_source_b454e115; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_source_b454e115 ON easy_thumbnails_source USING btree (storage_hash);


--
-- Name: easy_thumbnails_source_name_52f9bdf4bacaefed_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_source_name_52f9bdf4bacaefed_like ON easy_thumbnails_source USING btree (name varchar_pattern_ops);


--
-- Name: easy_thumbnails_source_storage_hash_74d89b9b49dfc360_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_source_storage_hash_74d89b9b49dfc360_like ON easy_thumbnails_source USING btree (storage_hash varchar_pattern_ops);


--
-- Name: easy_thumbnails_thumbnail_0afd9202; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_thumbnail_0afd9202 ON easy_thumbnails_thumbnail USING btree (source_id);


--
-- Name: easy_thumbnails_thumbnail_b068931c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_thumbnail_b068931c ON easy_thumbnails_thumbnail USING btree (name);


--
-- Name: easy_thumbnails_thumbnail_b454e115; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_thumbnail_b454e115 ON easy_thumbnails_thumbnail USING btree (storage_hash);


--
-- Name: easy_thumbnails_thumbnail_name_5cf9036e7f51237_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_thumbnail_name_5cf9036e7f51237_like ON easy_thumbnails_thumbnail USING btree (name varchar_pattern_ops);


--
-- Name: easy_thumbnails_thumbnail_storage_hash_1ef3b184ff542242_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_thumbnail_storage_hash_1ef3b184ff542242_like ON easy_thumbnails_thumbnail USING btree (storage_hash varchar_pattern_ops);


--
-- Name: filer_clipboard_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_clipboard_e8701ad4 ON filer_clipboard USING btree (user_id);


--
-- Name: filer_clipboarditem_2655b062; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_clipboarditem_2655b062 ON filer_clipboarditem USING btree (clipboard_id);


--
-- Name: filer_clipboarditem_814552b9; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_clipboarditem_814552b9 ON filer_clipboarditem USING btree (file_id);


--
-- Name: filer_file_5e7b1936; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_file_5e7b1936 ON filer_file USING btree (owner_id);


--
-- Name: filer_file_a8a44dbb; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_file_a8a44dbb ON filer_file USING btree (folder_id);


--
-- Name: filer_file_d3e32c49; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_file_d3e32c49 ON filer_file USING btree (polymorphic_ctype_id);


--
-- Name: filer_folder_3cfbd988; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folder_3cfbd988 ON filer_folder USING btree (rght);


--
-- Name: filer_folder_5e7b1936; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folder_5e7b1936 ON filer_folder USING btree (owner_id);


--
-- Name: filer_folder_656442a0; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folder_656442a0 ON filer_folder USING btree (tree_id);


--
-- Name: filer_folder_6be37982; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folder_6be37982 ON filer_folder USING btree (parent_id);


--
-- Name: filer_folder_c9e9a848; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folder_c9e9a848 ON filer_folder USING btree (level);


--
-- Name: filer_folder_caf7cc51; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folder_caf7cc51 ON filer_folder USING btree (lft);


--
-- Name: filer_folderpermission_0e939a4f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folderpermission_0e939a4f ON filer_folderpermission USING btree (group_id);


--
-- Name: filer_folderpermission_a8a44dbb; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folderpermission_a8a44dbb ON filer_folderpermission USING btree (folder_id);


--
-- Name: filer_folderpermission_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folderpermission_e8701ad4 ON filer_folderpermission USING btree (user_id);


--
-- Name: hosting_railsbetauser_email_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX hosting_railsbetauser_email_like ON hosting_railsbetauser USING btree (email varchar_pattern_ops);


--
-- Name: railshosting_railsbetauser_email_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX railshosting_railsbetauser_email_like ON railshosting_railsbetauser USING btree (email varchar_pattern_ops);


--
-- Name: reversion_revision_b16b0f06; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_revision_b16b0f06 ON reversion_revision USING btree (manager_slug);


--
-- Name: reversion_revision_c69e55a4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_revision_c69e55a4 ON reversion_revision USING btree (date_created);


--
-- Name: reversion_revision_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_revision_e8701ad4 ON reversion_revision USING btree (user_id);


--
-- Name: reversion_revision_manager_slug_26483faf947fe72_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_revision_manager_slug_26483faf947fe72_like ON reversion_revision USING btree (manager_slug varchar_pattern_ops);


--
-- Name: reversion_version_0c9ba3a3; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_version_0c9ba3a3 ON reversion_version USING btree (object_id_int);


--
-- Name: reversion_version_417f1b1c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_version_417f1b1c ON reversion_version USING btree (content_type_id);


--
-- Name: reversion_version_5de09a8d; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_version_5de09a8d ON reversion_version USING btree (revision_id);


--
-- Name: taggit_tag_name_7a358e5647db501d_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX taggit_tag_name_7a358e5647db501d_like ON taggit_tag USING btree (name varchar_pattern_ops);


--
-- Name: taggit_tag_slug_f7782df9b8e9952_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX taggit_tag_slug_f7782df9b8e9952_like ON taggit_tag USING btree (slug varchar_pattern_ops);


--
-- Name: taggit_taggeditem_417f1b1c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX taggit_taggeditem_417f1b1c ON taggit_taggeditem USING btree (content_type_id);


--
-- Name: taggit_taggeditem_76f094bc; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX taggit_taggeditem_76f094bc ON taggit_taggeditem USING btree (tag_id);


--
-- Name: taggit_taggeditem_af31437c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX taggit_taggeditem_af31437c ON taggit_taggeditem USING btree (object_id);


--
-- Name: taggit_taggeditem_content_type_id_6924a5bd6fce8bb9_idx; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX taggit_taggeditem_content_type_id_6924a5bd6fce8bb9_idx ON taggit_taggeditem USING btree (content_type_id, object_id);


--
-- Name: ungleich_ungleichpage_f33175e6; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX ungleich_ungleichpage_f33175e6 ON ungleich_ungleichpage USING btree (image_id);


--
-- Name: D045d6bc5122c2888af1542cc85348c8; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY ungleich_ungleichpage
    ADD CONSTRAINT "D045d6bc5122c2888af1542cc85348c8" FOREIGN KEY (public_extension_id) REFERENCES ungleich_ungleichpage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D18f0a3c282c7e09eda221cbd5e3192e; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_page_meta_titlemeta
    ADD CONSTRAINT "D18f0a3c282c7e09eda221cbd5e3192e" FOREIGN KEY (public_extension_id) REFERENCES djangocms_page_meta_titlemeta(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D1916c3dc15ac56bbecfb764e1edd4b6; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post
    ADD CONSTRAINT "D1916c3dc15ac56bbecfb764e1edd4b6" FOREIGN KEY (main_image_thumbnail_id) REFERENCES cmsplugin_filer_image_thumbnailoption(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D3db5af841b6175efb68810a56f3d71b; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_image_filerimage
    ADD CONSTRAINT "D3db5af841b6175efb68810a56f3d71b" FOREIGN KEY (thumbnail_option_id) REFERENCES cmsplugin_filer_image_thumbnailoption(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D3fcdca4e4fa94e57ca52e691e6e8bfa; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_categories
    ADD CONSTRAINT "D3fcdca4e4fa94e57ca52e691e6e8bfa" FOREIGN KEY (blogcategory_id) REFERENCES djangocms_blog_blogcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D4757fdafe2581c98401bff2c1f2a663; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_categories
    ADD CONSTRAINT "D4757fdafe2581c98401bff2c1f2a663" FOREIGN KEY (latestpostsplugin_id) REFERENCES djangocms_blog_latestpostsplugin(cmsplugin_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D546196e3170b816724a467c4984c357; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_file
    ADD CONSTRAINT "D546196e3170b816724a467c4984c357" FOREIGN KEY (polymorphic_ctype_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D74750ca7467fe005f3b759498e07742; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_page_meta_pagemeta
    ADD CONSTRAINT "D74750ca7467fe005f3b759498e07742" FOREIGN KEY (public_extension_id) REFERENCES djangocms_page_meta_pagemeta(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D771edfdb35443b0efed3c8426df14f8; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_tags
    ADD CONSTRAINT "D771edfdb35443b0efed3c8426df14f8" FOREIGN KEY (latestpostsplugin_id) REFERENCES djangocms_blog_latestpostsplugin(cmsplugin_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D80eb6ef4faf703498501f55a54f6eb8; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_categories
    ADD CONSTRAINT "D80eb6ef4faf703498501f55a54f6eb8" FOREIGN KEY (blogcategory_id) REFERENCES djangocms_blog_blogcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_content_type_id_64e1719ce5ca8a6d_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_content_type_id_64e1719ce5ca8a6d_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_p_permission_id_13f9ff776e0046_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_p_permission_id_13f9ff776e0046_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissio_group_id_3e5a5d7789ec3752_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_3e5a5d7789ec3752_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user__permission_id_60b91b178f4c450d_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user__permission_id_60b91b178f4c450d_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_605b0fc1af15748a_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_605b0fc1af15748a_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_6109f0f81ace7fe6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6109f0f81ace7fe6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permiss_user_id_485c61d21b4b4409_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permiss_user_id_485c61d21b4b4409_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: b4d7a3bfa619054ee8e3c72ee9dd548c; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_globalpagepermission_sites
    ADD CONSTRAINT b4d7a3bfa619054ee8e3c72ee9dd548c FOREIGN KEY (globalpagepermission_id) REFERENCES cms_globalpagepermission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_alias_cmsplugin_ptr_id_721e0f43634b6398_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_aliaspluginmodel
    ADD CONSTRAINT cms_alias_cmsplugin_ptr_id_721e0f43634b6398_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_alias_placeholder_id_3c065afe5855786b_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_aliaspluginmodel
    ADD CONSTRAINT cms_alias_placeholder_id_3c065afe5855786b_fk_cms_placeholder_id FOREIGN KEY (alias_placeholder_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_aliaspluginm_plugin_id_286ef06289c39b5c_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_aliaspluginmodel
    ADD CONSTRAINT cms_aliaspluginm_plugin_id_286ef06289c39b5c_fk_cms_cmsplugin_id FOREIGN KEY (plugin_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_cmsplu_placeholder_id_8718fbc4cd46e71_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmsplu_placeholder_id_8718fbc4cd46e71_fk_cms_placeholder_id FOREIGN KEY (placeholder_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_cmsplugin_parent_id_24b76873a88be0cb_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmsplugin_parent_id_24b76873a88be0cb_fk_cms_cmsplugin_id FOREIGN KEY (parent_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_globalpagepermis_group_id_7066bf1ccd6d7390_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_globalpagepermission
    ADD CONSTRAINT cms_globalpagepermis_group_id_7066bf1ccd6d7390_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_globalpagepermis_site_id_72a97057c2ea0a69_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_globalpagepermission_sites
    ADD CONSTRAINT cms_globalpagepermis_site_id_72a97057c2ea0a69_fk_django_site_id FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_globalpagepermissi_user_id_56bf56d4a8d5b0a0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_globalpagepermission
    ADD CONSTRAINT cms_globalpagepermissi_user_id_56bf56d4a8d5b0a0_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_p_placeholder_ref_id_7f5842a61f70973e_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_placeholderreference
    ADD CONSTRAINT cms_p_placeholder_ref_id_7f5842a61f70973e_fk_cms_placeholder_id FOREIGN KEY (placeholder_ref_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page__placeholder_id_5d6de1e3049053b0_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page_placeholders
    ADD CONSTRAINT cms_page__placeholder_id_5d6de1e3049053b0_fk_cms_placeholder_id FOREIGN KEY (placeholder_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page_parent_id_16d483330f2786b9_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_parent_id_16d483330f2786b9_fk_cms_page_id FOREIGN KEY (parent_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page_placeholders_page_id_5c1aabecb20513f1_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page_placeholders
    ADD CONSTRAINT cms_page_placeholders_page_id_5c1aabecb20513f1_fk_cms_page_id FOREIGN KEY (page_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page_publisher_public_id_7e7bca24d658a61c_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_publisher_public_id_7e7bca24d658a61c_fk_cms_page_id FOREIGN KEY (publisher_public_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page_site_id_51bc8ebff4261a88_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_site_id_51bc8ebff4261a88_fk_django_site_id FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pagepermission_group_id_14871c942c1ced3f_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pagepermission
    ADD CONSTRAINT cms_pagepermission_group_id_14871c942c1ced3f_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pagepermission_page_id_2b0ce7bdc2ae5b8_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pagepermission
    ADD CONSTRAINT cms_pagepermission_page_id_2b0ce7bdc2ae5b8_fk_cms_page_id FOREIGN KEY (page_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pagepermission_user_id_5feeedd6af240c6f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pagepermission
    ADD CONSTRAINT cms_pagepermission_user_id_5feeedd6af240c6f_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pageuser_created_by_id_71ea121116e84ad3_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pageuser
    ADD CONSTRAINT cms_pageuser_created_by_id_71ea121116e84ad3_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pageuser_user_ptr_id_340d3049fdd6daeb_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pageuser
    ADD CONSTRAINT cms_pageuser_user_ptr_id_340d3049fdd6daeb_fk_auth_user_id FOREIGN KEY (user_ptr_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pageusergrou_created_by_id_16b7873a739cdd41_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pageusergroup
    ADD CONSTRAINT cms_pageusergrou_created_by_id_16b7873a739cdd41_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pageusergroup_group_ptr_id_bbdd4a06a74d2ec_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pageusergroup
    ADD CONSTRAINT cms_pageusergroup_group_ptr_id_bbdd4a06a74d2ec_fk_auth_group_id FOREIGN KEY (group_ptr_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_place_cmsplugin_ptr_id_66379faa6a33f4ab_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_placeholderreference
    ADD CONSTRAINT cms_place_cmsplugin_ptr_id_66379faa6a33f4ab_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_staticplace_draft_id_32d5495aee4468b4_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplace_draft_id_32d5495aee4468b4_fk_cms_placeholder_id FOREIGN KEY (draft_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_staticplace_public_id_e26322c4c62bd7e_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplace_public_id_e26322c4c62bd7e_fk_cms_placeholder_id FOREIGN KEY (public_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_staticplaceholde_site_id_68762690d28d01d4_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplaceholde_site_id_68762690d28d01d4_fk_django_site_id FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_title_page_id_4ebd393d277199bf_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_page_id_4ebd393d277199bf_fk_cms_page_id FOREIGN KEY (page_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_title_publisher_public_id_27cecc46e5451469_fk_cms_title_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_publisher_public_id_27cecc46e5451469_fk_cms_title_id FOREIGN KEY (publisher_public_id) REFERENCES cms_title(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_userset_clipboard_id_720bd6f30e60bca8_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_usersettings
    ADD CONSTRAINT cms_userset_clipboard_id_720bd6f30e60bca8_fk_cms_placeholder_id FOREIGN KEY (clipboard_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_usersettings_user_id_5f1f22950c3ca2c8_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_usersettings
    ADD CONSTRAINT cms_usersettings_user_id_5f1f22950c3ca2c8_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin__image_id_2dd8c49eaf000c4a_fk_filer_image_file_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_teaser_filerteaser
    ADD CONSTRAINT cmsplugin__image_id_2dd8c49eaf000c4a_fk_filer_image_file_ptr_id FOREIGN KEY (image_id) REFERENCES filer_image(file_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin__image_id_6dcedb8ebed43032_fk_filer_image_file_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_video_filervideo
    ADD CONSTRAINT cmsplugin__image_id_6dcedb8ebed43032_fk_filer_image_file_ptr_id FOREIGN KEY (image_id) REFERENCES filer_image(file_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_cmsplugin_ptr_id_1614b969cfa257f1_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_teaser_filerteaser
    ADD CONSTRAINT cmsplugin_cmsplugin_ptr_id_1614b969cfa257f1_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_cmsplugin_ptr_id_1cc2a8f998c320bb_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_link_filerlinkplugin
    ADD CONSTRAINT cmsplugin_cmsplugin_ptr_id_1cc2a8f998c320bb_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_cmsplugin_ptr_id_2fef045737576d39_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_folder_filerfolder
    ADD CONSTRAINT cmsplugin_cmsplugin_ptr_id_2fef045737576d39_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_cmsplugin_ptr_id_3c44385c377a4db5_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_file_filerfile
    ADD CONSTRAINT cmsplugin_cmsplugin_ptr_id_3c44385c377a4db5_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_cmsplugin_ptr_id_4d6c50b300069d13_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_video_filervideo
    ADD CONSTRAINT cmsplugin_cmsplugin_ptr_id_4d6c50b300069d13_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_cmsplugin_ptr_id_686142e0c134e1d5_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_image_filerimage
    ADD CONSTRAINT cmsplugin_cmsplugin_ptr_id_686142e0c134e1d5_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_f_image_id_15a8d69b387a316_fk_filer_image_file_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_image_filerimage
    ADD CONSTRAINT cmsplugin_f_image_id_15a8d69b387a316_fk_filer_image_file_ptr_id FOREIGN KEY (image_id) REFERENCES filer_image(file_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer__file_link_id_7ae9937fd6074fe7_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_image_filerimage
    ADD CONSTRAINT cmsplugin_filer__file_link_id_7ae9937fd6074fe7_fk_filer_file_id FOREIGN KEY (file_link_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_file__file_id_1e92194b4cff1490_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_file_filerfile
    ADD CONSTRAINT cmsplugin_filer_file__file_id_1e92194b4cff1490_fk_filer_file_id FOREIGN KEY (file_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_fo_folder_id_b462dcd7da81054_fk_filer_folder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_folder_filerfolder
    ADD CONSTRAINT cmsplugin_filer_fo_folder_id_b462dcd7da81054_fk_filer_folder_id FOREIGN KEY (folder_id) REFERENCES filer_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_im_page_link_id_3ed262a1cd901da2_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_image_filerimage
    ADD CONSTRAINT cmsplugin_filer_im_page_link_id_3ed262a1cd901da2_fk_cms_page_id FOREIGN KEY (page_link_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_lin_page_link_id_332ee75546fa438_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_link_filerlinkplugin
    ADD CONSTRAINT cmsplugin_filer_lin_page_link_id_332ee75546fa438_fk_cms_page_id FOREIGN KEY (page_link_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_link__file_id_1c204ca30e9bcb80_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_link_filerlinkplugin
    ADD CONSTRAINT cmsplugin_filer_link__file_id_1c204ca30e9bcb80_fk_filer_file_id FOREIGN KEY (file_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_te_page_link_id_1140fe9baec531be_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_teaser_filerteaser
    ADD CONSTRAINT cmsplugin_filer_te_page_link_id_1140fe9baec531be_fk_cms_page_id FOREIGN KEY (page_link_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_vide_movie_id_1fa177f4e1f9a991_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_video_filervideo
    ADD CONSTRAINT cmsplugin_filer_vide_movie_id_1fa177f4e1f9a991_fk_filer_file_id FOREIGN KEY (movie_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: d12056587e1486d406b5b619b56c4dd0; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post
    ADD CONSTRAINT d12056587e1486d406b5b619b56c4dd0 FOREIGN KEY (main_image_full_id) REFERENCES cmsplugin_filer_image_thumbnailoption(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dig_dgGallery_id_2638f9236cdc8c98_fk_digitalglarus_dggallery_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY digitalglarus_dggalleryplugin
    ADD CONSTRAINT "dig_dgGallery_id_2638f9236cdc8c98_fk_digitalglarus_dggallery_id" FOREIGN KEY ("dgGallery_id") REFERENCES digitalglarus_dggallery(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: digita_gallery_id_88b90bbef747a6a_fk_digitalglarus_dggallery_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY digitalglarus_dgpicture
    ADD CONSTRAINT digita_gallery_id_88b90bbef747a6a_fk_digitalglarus_dggallery_id FOREIGN KEY (gallery_id) REFERENCES digitalglarus_dggallery(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: digital_parent_id_6a454e6ea73eb0e_fk_digitalglarus_dggallery_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY digitalglarus_dggallery
    ADD CONSTRAINT digital_parent_id_6a454e6ea73eb0e_fk_digitalglarus_dggallery_id FOREIGN KEY (parent_id) REFERENCES digitalglarus_dggallery(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: digitalgl_cmsplugin_ptr_id_570a61267a40961e_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY digitalglarus_dggalleryplugin
    ADD CONSTRAINT digitalgl_cmsplugin_ptr_id_570a61267a40961e_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: digitalgl_cmsplugin_ptr_id_6978110ddc0b7fd7_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY digitalglarus_dgsupportersplugin
    ADD CONSTRAINT digitalgl_cmsplugin_ptr_id_6978110ddc0b7fd7_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: digitalgla_image_id_2bdba91ba4e3a912_fk_filer_image_file_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY digitalglarus_dgpicture
    ADD CONSTRAINT digitalgla_image_id_2bdba91ba4e3a912_fk_filer_image_file_ptr_id FOREIGN KEY (image_id) REFERENCES filer_image(file_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dj_master_id_318c301265b12642_fk_djangocms_blog_blogcategory_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_blogcategory_translation
    ADD CONSTRAINT dj_master_id_318c301265b12642_fk_djangocms_blog_blogcategory_id FOREIGN KEY (master_id) REFERENCES djangocms_blog_blogcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dj_parent_id_5baa74cf2c7eca1d_fk_djangocms_blog_blogcategory_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_blogcategory
    ADD CONSTRAINT dj_parent_id_5baa74cf2c7eca1d_fk_djangocms_blog_blogcategory_id FOREIGN KEY (parent_id) REFERENCES djangocms_blog_blogcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dja_snippet_id_210c13c4c9097500_fk_djangocms_snippet_snippet_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_snippet_snippetptr
    ADD CONSTRAINT dja_snippet_id_210c13c4c9097500_fk_djangocms_snippet_snippet_id FOREIGN KEY (snippet_id) REFERENCES djangocms_snippet_snippet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djan_content_type_id_11d37054df52e2d0_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT djan_content_type_id_11d37054df52e2d0_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djang_main_image_id_46a449c9e90ca1a5_fk_filer_image_file_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post
    ADD CONSTRAINT djang_main_image_id_46a449c9e90ca1a5_fk_filer_image_file_ptr_id FOREIGN KEY (main_image_id) REFERENCES filer_image(file_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_376347ab24b09885_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_376347ab24b09885_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms__cmsplugin_ptr_id_3fe997e5bc4d562_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_snippet_snippetptr
    ADD CONSTRAINT djangocms__cmsplugin_ptr_id_3fe997e5bc4d562_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms__master_id_7202c6040792c48e_fk_djangocms_blog_post_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_translation
    ADD CONSTRAINT djangocms__master_id_7202c6040792c48e_fk_djangocms_blog_post_id FOREIGN KEY (master_id) REFERENCES djangocms_blog_post(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_bl_post_id_66886096ffa28c0e_fk_djangocms_blog_post_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_categories
    ADD CONSTRAINT djangocms_bl_post_id_66886096ffa28c0e_fk_djangocms_blog_post_id FOREIGN KEY (post_id) REFERENCES djangocms_blog_post(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_bl_post_id_7985888d2c6a9ec1_fk_djangocms_blog_post_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_sites
    ADD CONSTRAINT djangocms_bl_post_id_7985888d2c6a9ec1_fk_djangocms_blog_post_id FOREIGN KEY (post_id) REFERENCES djangocms_blog_post(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_blog_authore_user_id_4c051af7cdd4c6eb_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin_authors
    ADD CONSTRAINT djangocms_blog_authore_user_id_4c051af7cdd4c6eb_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_blog_content_id_75fcd6363f2c3a9_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post
    ADD CONSTRAINT djangocms_blog_content_id_75fcd6363f2c3a9_fk_cms_placeholder_id FOREIGN KEY (content_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_blog_latestp_tag_id_7732c8b615522b9f_fk_taggit_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_tags
    ADD CONSTRAINT djangocms_blog_latestp_tag_id_7732c8b615522b9f_fk_taggit_tag_id FOREIGN KEY (tag_id) REFERENCES taggit_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_blog_post__site_id_1acb65392bcb9089_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_sites
    ADD CONSTRAINT djangocms_blog_post__site_id_1acb65392bcb9089_fk_django_site_id FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_blog_post_author_id_1abe11362ada95f7_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post
    ADD CONSTRAINT djangocms_blog_post_author_id_1abe11362ada95f7_fk_auth_user_id FOREIGN KEY (author_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_216af445d5b32f9b_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_link_link
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_216af445d5b32f9b_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_2a9169bca11bd317_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_2a9169bca11bd317_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_3d1c8e1bb8a67ebf_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_flash_flash
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_3d1c8e1bb8a67ebf_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_4d6edbd3251ff534_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_teaser_teaser
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_4d6edbd3251ff534_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_507d115df608064c_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_507d115df608064c_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_5764a299a32edfd1_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_googlemap_googlemap
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_5764a299a32edfd1_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_5ed06a923d87711b_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_inherit_inheritpageplaceholder
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_5ed06a923d87711b_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_7f18aebaad9a37e6_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_text_ckeditor_text
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_7f18aebaad9a37e6_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_inherit_i_from_page_id_c7fc5ae030e1aa5_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_inherit_inheritpageplaceholder
    ADD CONSTRAINT djangocms_inherit_i_from_page_id_c7fc5ae030e1aa5_fk_cms_page_id FOREIGN KEY (from_page_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_link_lin_page_link_id_6910251473b4ce98_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_link_link
    ADD CONSTRAINT djangocms_link_lin_page_link_id_6910251473b4ce98_fk_cms_page_id FOREIGN KEY (page_link_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_p_extended_object_id_7f9e0a7f0b35accf_fk_cms_title_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_page_meta_titlemeta
    ADD CONSTRAINT djangocms_p_extended_object_id_7f9e0a7f0b35accf_fk_cms_title_id FOREIGN KEY (extended_object_id) REFERENCES cms_title(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_pag_extended_object_id_f30787f7ab972e3_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_page_meta_pagemeta
    ADD CONSTRAINT djangocms_pag_extended_object_id_f30787f7ab972e3_fk_cms_page_id FOREIGN KEY (extended_object_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_page_me_og_author_id_362eb37f4966a474_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_page_meta_pagemeta
    ADD CONSTRAINT djangocms_page_me_og_author_id_362eb37f4966a474_fk_auth_user_id FOREIGN KEY (og_author_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_page_meta__image_id_51134b68e1252deb_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_page_meta_pagemeta
    ADD CONSTRAINT djangocms_page_meta__image_id_51134b68e1252deb_fk_filer_file_id FOREIGN KEY (image_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_page_meta__image_id_7ea790a6ce828f17_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_page_meta_titlemeta
    ADD CONSTRAINT djangocms_page_meta__image_id_7ea790a6ce828f17_fk_filer_file_id FOREIGN KEY (image_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_teaser_t_page_link_id_7b28cbfa16b7dd61_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_teaser_teaser
    ADD CONSTRAINT djangocms_teaser_t_page_link_id_7b28cbfa16b7dd61_fk_cms_page_id FOREIGN KEY (page_link_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: e_thumbnail_id_540969c01e4bfdd3_fk_easy_thumbnails_thumbnail_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY easy_thumbnails_thumbnaildimensions
    ADD CONSTRAINT e_thumbnail_id_540969c01e4bfdd3_fk_easy_thumbnails_thumbnail_id FOREIGN KEY (thumbnail_id) REFERENCES easy_thumbnails_thumbnail(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: easy_th_source_id_697e1cd7af5c204a_fk_easy_thumbnails_source_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY easy_thumbnails_thumbnail
    ADD CONSTRAINT easy_th_source_id_697e1cd7af5c204a_fk_easy_thumbnails_source_id FOREIGN KEY (source_id) REFERENCES easy_thumbnails_source(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: f955851ee249e695fdae7f8fb50744b3; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin_authors
    ADD CONSTRAINT f955851ee249e695fdae7f8fb50744b3 FOREIGN KEY (authorentriesplugin_id) REFERENCES djangocms_blog_authorentriesplugin(cmsplugin_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_clipbo_clipboard_id_6af7d05a36e14dd_fk_filer_clipboard_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_clipboarditem
    ADD CONSTRAINT filer_clipbo_clipboard_id_6af7d05a36e14dd_fk_filer_clipboard_id FOREIGN KEY (clipboard_id) REFERENCES filer_clipboard(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_clipboard_user_id_50f26ea9a9fedaa0_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_clipboard
    ADD CONSTRAINT filer_clipboard_user_id_50f26ea9a9fedaa0_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_clipboarditem_file_id_7730cc2c9168b9c5_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_clipboarditem
    ADD CONSTRAINT filer_clipboarditem_file_id_7730cc2c9168b9c5_fk_filer_file_id FOREIGN KEY (file_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_file_folder_id_2ff5711011ec5cbb_fk_filer_folder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_file
    ADD CONSTRAINT filer_file_folder_id_2ff5711011ec5cbb_fk_filer_folder_id FOREIGN KEY (folder_id) REFERENCES filer_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_file_owner_id_34fc79468bea26b7_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_file
    ADD CONSTRAINT filer_file_owner_id_34fc79468bea26b7_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folder_owner_id_29a2ac62fb21e298_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folder
    ADD CONSTRAINT filer_folder_owner_id_29a2ac62fb21e298_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folder_parent_id_17f5ace114139133_fk_filer_folder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folder
    ADD CONSTRAINT filer_folder_parent_id_17f5ace114139133_fk_filer_folder_id FOREIGN KEY (parent_id) REFERENCES filer_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folderpermi_folder_id_60747a43810f1cd2_fk_filer_folder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folderpermission
    ADD CONSTRAINT filer_folderpermi_folder_id_60747a43810f1cd2_fk_filer_folder_id FOREIGN KEY (folder_id) REFERENCES filer_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folderpermissi_group_id_764df4dc0a7b9451_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folderpermission
    ADD CONSTRAINT filer_folderpermissi_group_id_764df4dc0a7b9451_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folderpermission_user_id_38fa74b7f36fc801_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folderpermission
    ADD CONSTRAINT filer_folderpermission_user_id_38fa74b7f36fc801_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_image_file_ptr_id_7d0adb8d6c9b8011_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_image
    ADD CONSTRAINT filer_image_file_ptr_id_7d0adb8d6c9b8011_fk_filer_file_id FOREIGN KEY (file_ptr_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reve_content_type_id_49be33e388776bc1_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY reversion_version
    ADD CONSTRAINT reve_content_type_id_49be33e388776bc1_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reversion_revision_id_1589de84f8370d65_fk_reversion_revision_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY reversion_version
    ADD CONSTRAINT reversion_revision_id_1589de84f8370d65_fk_reversion_revision_id FOREIGN KEY (revision_id) REFERENCES reversion_revision(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reversion_revision_user_id_3cb6e6a5acf9ad5f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY reversion_revision
    ADD CONSTRAINT reversion_revision_user_id_3cb6e6a5acf9ad5f_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tagg_content_type_id_647783b6f2ffd739_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT tagg_content_type_id_647783b6f2ffd739_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taggit_taggeditem_tag_id_732e18aba056f370_fk_taggit_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_tag_id_732e18aba056f370_fk_taggit_tag_id FOREIGN KEY (tag_id) REFERENCES taggit_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ungleich_u_image_id_377a61544fc69cef_fk_filer_image_file_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY ungleich_ungleichpage
    ADD CONSTRAINT ungleich_u_image_id_377a61544fc69cef_fk_filer_image_file_ptr_id FOREIGN KEY (image_id) REFERENCES filer_image(file_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ungleich_ung_extended_object_id_6304137b758d935b_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY ungleich_ungleichpage
    ADD CONSTRAINT ungleich_ung_extended_object_id_6304137b758d935b_fk_cms_page_id FOREIGN KEY (extended_object_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\connect appdb

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\connect dynamicweb

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE auth_group OWNER TO app;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_id_seq OWNER TO app;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_group_permissions OWNER TO app;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_permissions_id_seq OWNER TO app;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE auth_permission OWNER TO app;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_permission_id_seq OWNER TO app;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE auth_user OWNER TO app;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE auth_user_groups OWNER TO app;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_groups_id_seq OWNER TO app;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_id_seq OWNER TO app;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_user_user_permissions OWNER TO app;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_user_permissions_id_seq OWNER TO app;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: cms_aliaspluginmodel; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_aliaspluginmodel (
    cmsplugin_ptr_id integer NOT NULL,
    plugin_id integer,
    alias_placeholder_id integer
);


ALTER TABLE cms_aliaspluginmodel OWNER TO app;

--
-- Name: cms_cmsplugin; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_cmsplugin (
    id integer NOT NULL,
    "position" smallint,
    language character varying(15) NOT NULL,
    plugin_type character varying(50) NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    changed_date timestamp with time zone NOT NULL,
    parent_id integer,
    placeholder_id integer,
    depth integer NOT NULL,
    numchild integer NOT NULL,
    path character varying(255) NOT NULL,
    CONSTRAINT cms_cmsplugin_depth_check CHECK ((depth >= 0)),
    CONSTRAINT cms_cmsplugin_numchild_check CHECK ((numchild >= 0)),
    CONSTRAINT cms_cmsplugin_position_check CHECK (("position" >= 0))
);


ALTER TABLE cms_cmsplugin OWNER TO app;

--
-- Name: cms_cmsplugin_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_cmsplugin_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_cmsplugin_id_seq OWNER TO app;

--
-- Name: cms_cmsplugin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_cmsplugin_id_seq OWNED BY cms_cmsplugin.id;


--
-- Name: cms_globalpagepermission; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_globalpagepermission (
    id integer NOT NULL,
    can_change boolean NOT NULL,
    can_add boolean NOT NULL,
    can_delete boolean NOT NULL,
    can_change_advanced_settings boolean NOT NULL,
    can_publish boolean NOT NULL,
    can_change_permissions boolean NOT NULL,
    can_move_page boolean NOT NULL,
    can_view boolean NOT NULL,
    can_recover_page boolean NOT NULL,
    group_id integer,
    user_id integer
);


ALTER TABLE cms_globalpagepermission OWNER TO app;

--
-- Name: cms_globalpagepermission_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_globalpagepermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_globalpagepermission_id_seq OWNER TO app;

--
-- Name: cms_globalpagepermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_globalpagepermission_id_seq OWNED BY cms_globalpagepermission.id;


--
-- Name: cms_globalpagepermission_sites; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_globalpagepermission_sites (
    id integer NOT NULL,
    globalpagepermission_id integer NOT NULL,
    site_id integer NOT NULL
);


ALTER TABLE cms_globalpagepermission_sites OWNER TO app;

--
-- Name: cms_globalpagepermission_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_globalpagepermission_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_globalpagepermission_sites_id_seq OWNER TO app;

--
-- Name: cms_globalpagepermission_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_globalpagepermission_sites_id_seq OWNED BY cms_globalpagepermission_sites.id;


--
-- Name: cms_page; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_page (
    id integer NOT NULL,
    created_by character varying(255) NOT NULL,
    changed_by character varying(255) NOT NULL,
    creation_date timestamp with time zone NOT NULL,
    changed_date timestamp with time zone NOT NULL,
    publication_date timestamp with time zone,
    publication_end_date timestamp with time zone,
    in_navigation boolean NOT NULL,
    soft_root boolean NOT NULL,
    reverse_id character varying(40),
    navigation_extenders character varying(80),
    template character varying(100) NOT NULL,
    login_required boolean NOT NULL,
    limit_visibility_in_menu smallint,
    is_home boolean NOT NULL,
    application_urls character varying(200),
    application_namespace character varying(200),
    publisher_is_draft boolean NOT NULL,
    languages character varying(255),
    revision_id integer NOT NULL,
    xframe_options integer NOT NULL,
    parent_id integer,
    publisher_public_id integer,
    site_id integer NOT NULL,
    depth integer NOT NULL,
    numchild integer NOT NULL,
    path character varying(255) NOT NULL,
    CONSTRAINT cms_page_depth_check CHECK ((depth >= 0)),
    CONSTRAINT cms_page_numchild_check CHECK ((numchild >= 0)),
    CONSTRAINT cms_page_revision_id_check CHECK ((revision_id >= 0))
);


ALTER TABLE cms_page OWNER TO app;

--
-- Name: cms_page_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_page_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_page_id_seq OWNER TO app;

--
-- Name: cms_page_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_page_id_seq OWNED BY cms_page.id;


--
-- Name: cms_page_placeholders; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_page_placeholders (
    id integer NOT NULL,
    page_id integer NOT NULL,
    placeholder_id integer NOT NULL
);


ALTER TABLE cms_page_placeholders OWNER TO app;

--
-- Name: cms_page_placeholders_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_page_placeholders_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_page_placeholders_id_seq OWNER TO app;

--
-- Name: cms_page_placeholders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_page_placeholders_id_seq OWNED BY cms_page_placeholders.id;


--
-- Name: cms_pagepermission; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_pagepermission (
    id integer NOT NULL,
    can_change boolean NOT NULL,
    can_add boolean NOT NULL,
    can_delete boolean NOT NULL,
    can_change_advanced_settings boolean NOT NULL,
    can_publish boolean NOT NULL,
    can_change_permissions boolean NOT NULL,
    can_move_page boolean NOT NULL,
    can_view boolean NOT NULL,
    grant_on integer NOT NULL,
    group_id integer,
    page_id integer,
    user_id integer
);


ALTER TABLE cms_pagepermission OWNER TO app;

--
-- Name: cms_pagepermission_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_pagepermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_pagepermission_id_seq OWNER TO app;

--
-- Name: cms_pagepermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_pagepermission_id_seq OWNED BY cms_pagepermission.id;


--
-- Name: cms_pageuser; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_pageuser (
    user_ptr_id integer NOT NULL,
    created_by_id integer NOT NULL
);


ALTER TABLE cms_pageuser OWNER TO app;

--
-- Name: cms_pageusergroup; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_pageusergroup (
    group_ptr_id integer NOT NULL,
    created_by_id integer NOT NULL
);


ALTER TABLE cms_pageusergroup OWNER TO app;

--
-- Name: cms_placeholder; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_placeholder (
    id integer NOT NULL,
    slot character varying(255) NOT NULL,
    default_width smallint,
    CONSTRAINT cms_placeholder_default_width_check CHECK ((default_width >= 0))
);


ALTER TABLE cms_placeholder OWNER TO app;

--
-- Name: cms_placeholder_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_placeholder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_placeholder_id_seq OWNER TO app;

--
-- Name: cms_placeholder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_placeholder_id_seq OWNED BY cms_placeholder.id;


--
-- Name: cms_placeholderreference; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_placeholderreference (
    cmsplugin_ptr_id integer NOT NULL,
    name character varying(255) NOT NULL,
    placeholder_ref_id integer
);


ALTER TABLE cms_placeholderreference OWNER TO app;

--
-- Name: cms_staticplaceholder; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_staticplaceholder (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    code character varying(255) NOT NULL,
    dirty boolean NOT NULL,
    creation_method character varying(20) NOT NULL,
    draft_id integer,
    public_id integer,
    site_id integer
);


ALTER TABLE cms_staticplaceholder OWNER TO app;

--
-- Name: cms_staticplaceholder_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_staticplaceholder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_staticplaceholder_id_seq OWNER TO app;

--
-- Name: cms_staticplaceholder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_staticplaceholder_id_seq OWNED BY cms_staticplaceholder.id;


--
-- Name: cms_title; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_title (
    id integer NOT NULL,
    language character varying(15) NOT NULL,
    title character varying(255) NOT NULL,
    page_title character varying(255),
    menu_title character varying(255),
    meta_description text,
    slug character varying(255) NOT NULL,
    path character varying(255) NOT NULL,
    has_url_overwrite boolean NOT NULL,
    redirect character varying(2048),
    creation_date timestamp with time zone NOT NULL,
    published boolean NOT NULL,
    publisher_is_draft boolean NOT NULL,
    publisher_state smallint NOT NULL,
    page_id integer NOT NULL,
    publisher_public_id integer
);


ALTER TABLE cms_title OWNER TO app;

--
-- Name: cms_title_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_title_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_title_id_seq OWNER TO app;

--
-- Name: cms_title_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_title_id_seq OWNED BY cms_title.id;


--
-- Name: cms_usersettings; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cms_usersettings (
    id integer NOT NULL,
    language character varying(10) NOT NULL,
    clipboard_id integer,
    user_id integer NOT NULL
);


ALTER TABLE cms_usersettings OWNER TO app;

--
-- Name: cms_usersettings_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cms_usersettings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cms_usersettings_id_seq OWNER TO app;

--
-- Name: cms_usersettings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cms_usersettings_id_seq OWNED BY cms_usersettings.id;


--
-- Name: cmsplugin_filer_file_filerfile; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_file_filerfile (
    cmsplugin_ptr_id integer NOT NULL,
    title character varying(255),
    target_blank boolean NOT NULL,
    style character varying(255) NOT NULL,
    file_id integer NOT NULL
);


ALTER TABLE cmsplugin_filer_file_filerfile OWNER TO app;

--
-- Name: cmsplugin_filer_folder_filerfolder; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_folder_filerfolder (
    cmsplugin_ptr_id integer NOT NULL,
    title character varying(255),
    style character varying(50) NOT NULL,
    folder_id integer NOT NULL
);


ALTER TABLE cmsplugin_filer_folder_filerfolder OWNER TO app;

--
-- Name: cmsplugin_filer_image_filerimage; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_image_filerimage (
    cmsplugin_ptr_id integer NOT NULL,
    style character varying(50) NOT NULL,
    caption_text character varying(255),
    image_url character varying(200),
    alt_text character varying(255),
    use_original_image boolean NOT NULL,
    use_autoscale boolean NOT NULL,
    width integer,
    height integer,
    crop boolean NOT NULL,
    upscale boolean NOT NULL,
    alignment character varying(10),
    free_link character varying(255),
    original_link boolean NOT NULL,
    description text,
    target_blank boolean NOT NULL,
    file_link_id integer,
    image_id integer,
    page_link_id integer,
    thumbnail_option_id integer,
    CONSTRAINT cmsplugin_filer_image_filerimage_height_check CHECK ((height >= 0)),
    CONSTRAINT cmsplugin_filer_image_filerimage_width_check CHECK ((width >= 0))
);


ALTER TABLE cmsplugin_filer_image_filerimage OWNER TO app;

--
-- Name: cmsplugin_filer_image_thumbnailoption; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_image_thumbnailoption (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    width integer NOT NULL,
    height integer NOT NULL,
    crop boolean NOT NULL,
    upscale boolean NOT NULL
);


ALTER TABLE cmsplugin_filer_image_thumbnailoption OWNER TO app;

--
-- Name: cmsplugin_filer_image_thumbnailoption_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE cmsplugin_filer_image_thumbnailoption_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE cmsplugin_filer_image_thumbnailoption_id_seq OWNER TO app;

--
-- Name: cmsplugin_filer_image_thumbnailoption_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE cmsplugin_filer_image_thumbnailoption_id_seq OWNED BY cmsplugin_filer_image_thumbnailoption.id;


--
-- Name: cmsplugin_filer_link_filerlinkplugin; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_link_filerlinkplugin (
    cmsplugin_ptr_id integer NOT NULL,
    name character varying(255) NOT NULL,
    url character varying(255),
    mailto character varying(75),
    link_style character varying(255) NOT NULL,
    new_window boolean NOT NULL,
    file_id integer,
    page_link_id integer
);


ALTER TABLE cmsplugin_filer_link_filerlinkplugin OWNER TO app;

--
-- Name: cmsplugin_filer_teaser_filerteaser; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_teaser_filerteaser (
    cmsplugin_ptr_id integer NOT NULL,
    title character varying(255) NOT NULL,
    image_url character varying(200),
    style character varying(255) NOT NULL,
    use_autoscale boolean NOT NULL,
    width integer,
    height integer,
    free_link character varying(255),
    description text,
    target_blank boolean NOT NULL,
    image_id integer,
    page_link_id integer,
    CONSTRAINT cmsplugin_filer_teaser_filerteaser_height_check CHECK ((height >= 0)),
    CONSTRAINT cmsplugin_filer_teaser_filerteaser_width_check CHECK ((width >= 0))
);


ALTER TABLE cmsplugin_filer_teaser_filerteaser OWNER TO app;

--
-- Name: cmsplugin_filer_video_filervideo; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE cmsplugin_filer_video_filervideo (
    cmsplugin_ptr_id integer NOT NULL,
    movie_url character varying(255),
    width smallint NOT NULL,
    height smallint NOT NULL,
    auto_play boolean NOT NULL,
    auto_hide boolean NOT NULL,
    fullscreen boolean NOT NULL,
    loop boolean NOT NULL,
    bgcolor character varying(6) NOT NULL,
    textcolor character varying(6) NOT NULL,
    seekbarcolor character varying(6) NOT NULL,
    seekbarbgcolor character varying(6) NOT NULL,
    loadingbarcolor character varying(6) NOT NULL,
    buttonoutcolor character varying(6) NOT NULL,
    buttonovercolor character varying(6) NOT NULL,
    buttonhighlightcolor character varying(6) NOT NULL,
    image_id integer,
    movie_id integer,
    CONSTRAINT cmsplugin_filer_video_filervideo_height_check CHECK ((height >= 0)),
    CONSTRAINT cmsplugin_filer_video_filervideo_width_check CHECK ((width >= 0))
);


ALTER TABLE cmsplugin_filer_video_filervideo OWNER TO app;

--
-- Name: digital_glarus_message; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE digital_glarus_message (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    email character varying(75) NOT NULL,
    phone_number character varying(200) NOT NULL,
    message text NOT NULL,
    received_date timestamp with time zone NOT NULL
);


ALTER TABLE digital_glarus_message OWNER TO app;

--
-- Name: digital_glarus_message_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE digital_glarus_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE digital_glarus_message_id_seq OWNER TO app;

--
-- Name: digital_glarus_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE digital_glarus_message_id_seq OWNED BY digital_glarus_message.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE django_admin_log OWNER TO app;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_admin_log_id_seq OWNER TO app;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO app;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_content_type_id_seq OWNER TO app;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO app;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO app;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_select2_keymap; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE django_select2_keymap (
    id integer NOT NULL,
    key character varying(40) NOT NULL,
    value character varying(100) NOT NULL,
    accessed_on timestamp with time zone NOT NULL
);


ALTER TABLE django_select2_keymap OWNER TO app;

--
-- Name: django_select2_keymap_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE django_select2_keymap_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_select2_keymap_id_seq OWNER TO app;

--
-- Name: django_select2_keymap_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE django_select2_keymap_id_seq OWNED BY django_select2_keymap.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE django_session OWNER TO app;

--
-- Name: django_site; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE django_site OWNER TO app;

--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_site_id_seq OWNER TO app;

--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: djangocms_blog_authorentriesplugin; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_authorentriesplugin (
    cmsplugin_ptr_id integer NOT NULL,
    latest_posts integer NOT NULL
);


ALTER TABLE djangocms_blog_authorentriesplugin OWNER TO app;

--
-- Name: djangocms_blog_authorentriesplugin_authors; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_authorentriesplugin_authors (
    id integer NOT NULL,
    authorentriesplugin_id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE djangocms_blog_authorentriesplugin_authors OWNER TO app;

--
-- Name: djangocms_blog_authorentriesplugin_authors_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_authorentriesplugin_authors_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_authorentriesplugin_authors_id_seq OWNER TO app;

--
-- Name: djangocms_blog_authorentriesplugin_authors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_authorentriesplugin_authors_id_seq OWNED BY djangocms_blog_authorentriesplugin_authors.id;


--
-- Name: djangocms_blog_blogcategory; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_blogcategory (
    id integer NOT NULL,
    date_created timestamp with time zone NOT NULL,
    date_modified timestamp with time zone NOT NULL,
    parent_id integer
);


ALTER TABLE djangocms_blog_blogcategory OWNER TO app;

--
-- Name: djangocms_blog_blogcategory_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_blogcategory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_blogcategory_id_seq OWNER TO app;

--
-- Name: djangocms_blog_blogcategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_blogcategory_id_seq OWNED BY djangocms_blog_blogcategory.id;


--
-- Name: djangocms_blog_blogcategory_translation; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_blogcategory_translation (
    id integer NOT NULL,
    language_code character varying(15) NOT NULL,
    name character varying(255) NOT NULL,
    slug character varying(50) NOT NULL,
    master_id integer
);


ALTER TABLE djangocms_blog_blogcategory_translation OWNER TO app;

--
-- Name: djangocms_blog_blogcategory_translation_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_blogcategory_translation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_blogcategory_translation_id_seq OWNER TO app;

--
-- Name: djangocms_blog_blogcategory_translation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_blogcategory_translation_id_seq OWNED BY djangocms_blog_blogcategory_translation.id;


--
-- Name: djangocms_blog_latestpostsplugin; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_latestpostsplugin (
    cmsplugin_ptr_id integer NOT NULL,
    latest_posts integer NOT NULL
);


ALTER TABLE djangocms_blog_latestpostsplugin OWNER TO app;

--
-- Name: djangocms_blog_latestpostsplugin_categories; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_latestpostsplugin_categories (
    id integer NOT NULL,
    latestpostsplugin_id integer NOT NULL,
    blogcategory_id integer NOT NULL
);


ALTER TABLE djangocms_blog_latestpostsplugin_categories OWNER TO app;

--
-- Name: djangocms_blog_latestpostsplugin_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_latestpostsplugin_categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_latestpostsplugin_categories_id_seq OWNER TO app;

--
-- Name: djangocms_blog_latestpostsplugin_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_latestpostsplugin_categories_id_seq OWNED BY djangocms_blog_latestpostsplugin_categories.id;


--
-- Name: djangocms_blog_latestpostsplugin_tags; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_latestpostsplugin_tags (
    id integer NOT NULL,
    latestpostsplugin_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE djangocms_blog_latestpostsplugin_tags OWNER TO app;

--
-- Name: djangocms_blog_latestpostsplugin_tags_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_latestpostsplugin_tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_latestpostsplugin_tags_id_seq OWNER TO app;

--
-- Name: djangocms_blog_latestpostsplugin_tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_latestpostsplugin_tags_id_seq OWNED BY djangocms_blog_latestpostsplugin_tags.id;


--
-- Name: djangocms_blog_post; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_post (
    id integer NOT NULL,
    date_created timestamp with time zone NOT NULL,
    date_modified timestamp with time zone NOT NULL,
    date_published timestamp with time zone NOT NULL,
    date_published_end timestamp with time zone,
    publish boolean NOT NULL,
    enable_comments boolean NOT NULL,
    author_id integer,
    content_id integer,
    main_image_id integer,
    main_image_full_id integer,
    main_image_thumbnail_id integer
);


ALTER TABLE djangocms_blog_post OWNER TO app;

--
-- Name: djangocms_blog_post_categories; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_post_categories (
    id integer NOT NULL,
    post_id integer NOT NULL,
    blogcategory_id integer NOT NULL
);


ALTER TABLE djangocms_blog_post_categories OWNER TO app;

--
-- Name: djangocms_blog_post_categories_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_post_categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_post_categories_id_seq OWNER TO app;

--
-- Name: djangocms_blog_post_categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_post_categories_id_seq OWNED BY djangocms_blog_post_categories.id;


--
-- Name: djangocms_blog_post_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_post_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_post_id_seq OWNER TO app;

--
-- Name: djangocms_blog_post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_post_id_seq OWNED BY djangocms_blog_post.id;


--
-- Name: djangocms_blog_post_sites; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_post_sites (
    id integer NOT NULL,
    post_id integer NOT NULL,
    site_id integer NOT NULL
);


ALTER TABLE djangocms_blog_post_sites OWNER TO app;

--
-- Name: djangocms_blog_post_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_post_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_post_sites_id_seq OWNER TO app;

--
-- Name: djangocms_blog_post_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_post_sites_id_seq OWNED BY djangocms_blog_post_sites.id;


--
-- Name: djangocms_blog_post_translation; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_blog_post_translation (
    id integer NOT NULL,
    language_code character varying(15) NOT NULL,
    title character varying(255) NOT NULL,
    slug character varying(50) NOT NULL,
    abstract text NOT NULL,
    meta_description text NOT NULL,
    meta_keywords text NOT NULL,
    meta_title character varying(255) NOT NULL,
    post_text text NOT NULL,
    master_id integer
);


ALTER TABLE djangocms_blog_post_translation OWNER TO app;

--
-- Name: djangocms_blog_post_translation_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_blog_post_translation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_blog_post_translation_id_seq OWNER TO app;

--
-- Name: djangocms_blog_post_translation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_blog_post_translation_id_seq OWNED BY djangocms_blog_post_translation.id;


--
-- Name: djangocms_flash_flash; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_flash_flash (
    cmsplugin_ptr_id integer NOT NULL,
    file character varying(100) NOT NULL,
    width character varying(6) NOT NULL,
    height character varying(6) NOT NULL
);


ALTER TABLE djangocms_flash_flash OWNER TO app;

--
-- Name: djangocms_googlemap_googlemap; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_googlemap_googlemap (
    cmsplugin_ptr_id integer NOT NULL,
    title character varying(100),
    address character varying(150) NOT NULL,
    zipcode character varying(30) NOT NULL,
    city character varying(100) NOT NULL,
    content character varying(255) NOT NULL,
    zoom smallint NOT NULL,
    lat numeric(10,6),
    lng numeric(10,6),
    route_planer_title character varying(150),
    route_planer boolean NOT NULL,
    width character varying(6) NOT NULL,
    height character varying(6) NOT NULL,
    info_window boolean NOT NULL,
    scrollwheel boolean NOT NULL,
    double_click_zoom boolean NOT NULL,
    draggable boolean NOT NULL,
    keyboard_shortcuts boolean NOT NULL,
    pan_control boolean NOT NULL,
    zoom_control boolean NOT NULL,
    street_view_control boolean NOT NULL,
    CONSTRAINT djangocms_googlemap_googlemap_zoom_check CHECK ((zoom >= 0))
);


ALTER TABLE djangocms_googlemap_googlemap OWNER TO app;

--
-- Name: djangocms_inherit_inheritpageplaceholder; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_inherit_inheritpageplaceholder (
    cmsplugin_ptr_id integer NOT NULL,
    from_language character varying(5),
    from_page_id integer
);


ALTER TABLE djangocms_inherit_inheritpageplaceholder OWNER TO app;

--
-- Name: djangocms_link_link; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_link_link (
    cmsplugin_ptr_id integer NOT NULL,
    name character varying(256) NOT NULL,
    url character varying(200),
    anchor character varying(128) NOT NULL,
    mailto character varying(75),
    phone character varying(40),
    target character varying(100) NOT NULL,
    page_link_id integer
);


ALTER TABLE djangocms_link_link OWNER TO app;

--
-- Name: djangocms_snippet_snippet; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_snippet_snippet (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    html text NOT NULL,
    template character varying(50) NOT NULL
);


ALTER TABLE djangocms_snippet_snippet OWNER TO app;

--
-- Name: djangocms_snippet_snippet_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE djangocms_snippet_snippet_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE djangocms_snippet_snippet_id_seq OWNER TO app;

--
-- Name: djangocms_snippet_snippet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE djangocms_snippet_snippet_id_seq OWNED BY djangocms_snippet_snippet.id;


--
-- Name: djangocms_snippet_snippetptr; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_snippet_snippetptr (
    cmsplugin_ptr_id integer NOT NULL,
    snippet_id integer NOT NULL
);


ALTER TABLE djangocms_snippet_snippetptr OWNER TO app;

--
-- Name: djangocms_teaser_teaser; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_teaser_teaser (
    cmsplugin_ptr_id integer NOT NULL,
    title character varying(255) NOT NULL,
    image character varying(100),
    url character varying(255),
    description text,
    page_link_id integer
);


ALTER TABLE djangocms_teaser_teaser OWNER TO app;

--
-- Name: djangocms_text_ckeditor_text; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE djangocms_text_ckeditor_text (
    cmsplugin_ptr_id integer NOT NULL,
    body text NOT NULL
);


ALTER TABLE djangocms_text_ckeditor_text OWNER TO app;

--
-- Name: easy_thumbnails_source; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE easy_thumbnails_source (
    id integer NOT NULL,
    storage_hash character varying(40) NOT NULL,
    name character varying(255) NOT NULL,
    modified timestamp with time zone NOT NULL
);


ALTER TABLE easy_thumbnails_source OWNER TO app;

--
-- Name: easy_thumbnails_source_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE easy_thumbnails_source_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE easy_thumbnails_source_id_seq OWNER TO app;

--
-- Name: easy_thumbnails_source_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE easy_thumbnails_source_id_seq OWNED BY easy_thumbnails_source.id;


--
-- Name: easy_thumbnails_thumbnail; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE easy_thumbnails_thumbnail (
    id integer NOT NULL,
    storage_hash character varying(40) NOT NULL,
    name character varying(255) NOT NULL,
    modified timestamp with time zone NOT NULL,
    source_id integer NOT NULL
);


ALTER TABLE easy_thumbnails_thumbnail OWNER TO app;

--
-- Name: easy_thumbnails_thumbnail_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE easy_thumbnails_thumbnail_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE easy_thumbnails_thumbnail_id_seq OWNER TO app;

--
-- Name: easy_thumbnails_thumbnail_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE easy_thumbnails_thumbnail_id_seq OWNED BY easy_thumbnails_thumbnail.id;


--
-- Name: easy_thumbnails_thumbnaildimensions; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE easy_thumbnails_thumbnaildimensions (
    id integer NOT NULL,
    thumbnail_id integer NOT NULL,
    width integer,
    height integer,
    CONSTRAINT easy_thumbnails_thumbnaildimensions_height_check CHECK ((height >= 0)),
    CONSTRAINT easy_thumbnails_thumbnaildimensions_width_check CHECK ((width >= 0))
);


ALTER TABLE easy_thumbnails_thumbnaildimensions OWNER TO app;

--
-- Name: easy_thumbnails_thumbnaildimensions_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE easy_thumbnails_thumbnaildimensions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE easy_thumbnails_thumbnaildimensions_id_seq OWNER TO app;

--
-- Name: easy_thumbnails_thumbnaildimensions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE easy_thumbnails_thumbnaildimensions_id_seq OWNED BY easy_thumbnails_thumbnaildimensions.id;


--
-- Name: filer_clipboard; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE filer_clipboard (
    id integer NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE filer_clipboard OWNER TO app;

--
-- Name: filer_clipboard_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE filer_clipboard_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE filer_clipboard_id_seq OWNER TO app;

--
-- Name: filer_clipboard_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE filer_clipboard_id_seq OWNED BY filer_clipboard.id;


--
-- Name: filer_clipboarditem; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE filer_clipboarditem (
    id integer NOT NULL,
    clipboard_id integer NOT NULL,
    file_id integer NOT NULL
);


ALTER TABLE filer_clipboarditem OWNER TO app;

--
-- Name: filer_clipboarditem_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE filer_clipboarditem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE filer_clipboarditem_id_seq OWNER TO app;

--
-- Name: filer_clipboarditem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE filer_clipboarditem_id_seq OWNED BY filer_clipboarditem.id;


--
-- Name: filer_file; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE filer_file (
    id integer NOT NULL,
    file character varying(255),
    _file_size integer,
    sha1 character varying(40) NOT NULL,
    has_all_mandatory_data boolean NOT NULL,
    original_filename character varying(255),
    name character varying(255) NOT NULL,
    description text,
    uploaded_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    is_public boolean NOT NULL,
    folder_id integer,
    owner_id integer,
    polymorphic_ctype_id integer
);


ALTER TABLE filer_file OWNER TO app;

--
-- Name: filer_file_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE filer_file_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE filer_file_id_seq OWNER TO app;

--
-- Name: filer_file_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE filer_file_id_seq OWNED BY filer_file.id;


--
-- Name: filer_folder; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE filer_folder (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    uploaded_at timestamp with time zone NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    lft integer NOT NULL,
    rght integer NOT NULL,
    tree_id integer NOT NULL,
    level integer NOT NULL,
    owner_id integer,
    parent_id integer,
    CONSTRAINT filer_folder_level_check CHECK ((level >= 0)),
    CONSTRAINT filer_folder_lft_check CHECK ((lft >= 0)),
    CONSTRAINT filer_folder_rght_check CHECK ((rght >= 0)),
    CONSTRAINT filer_folder_tree_id_check CHECK ((tree_id >= 0))
);


ALTER TABLE filer_folder OWNER TO app;

--
-- Name: filer_folder_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE filer_folder_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE filer_folder_id_seq OWNER TO app;

--
-- Name: filer_folder_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE filer_folder_id_seq OWNED BY filer_folder.id;


--
-- Name: filer_folderpermission; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE filer_folderpermission (
    id integer NOT NULL,
    type smallint NOT NULL,
    everybody boolean NOT NULL,
    can_edit smallint,
    can_read smallint,
    can_add_children smallint,
    folder_id integer,
    group_id integer,
    user_id integer
);


ALTER TABLE filer_folderpermission OWNER TO app;

--
-- Name: filer_folderpermission_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE filer_folderpermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE filer_folderpermission_id_seq OWNER TO app;

--
-- Name: filer_folderpermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE filer_folderpermission_id_seq OWNED BY filer_folderpermission.id;


--
-- Name: filer_image; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE filer_image (
    file_ptr_id integer NOT NULL,
    _height integer,
    _width integer,
    date_taken timestamp with time zone,
    default_alt_text character varying(255),
    default_caption character varying(255),
    author character varying(255),
    must_always_publish_author_credit boolean NOT NULL,
    must_always_publish_copyright boolean NOT NULL,
    subject_location character varying(64)
);


ALTER TABLE filer_image OWNER TO app;

--
-- Name: menus_cachekey; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE menus_cachekey (
    id integer NOT NULL,
    language character varying(255) NOT NULL,
    site integer NOT NULL,
    key character varying(255) NOT NULL,
    CONSTRAINT menus_cachekey_site_check CHECK ((site >= 0))
);


ALTER TABLE menus_cachekey OWNER TO app;

--
-- Name: menus_cachekey_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE menus_cachekey_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE menus_cachekey_id_seq OWNER TO app;

--
-- Name: menus_cachekey_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE menus_cachekey_id_seq OWNED BY menus_cachekey.id;


--
-- Name: railshosting_railsbetauser; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE railshosting_railsbetauser (
    id integer NOT NULL,
    email character varying(75) NOT NULL,
    received_date timestamp with time zone NOT NULL
);


ALTER TABLE railshosting_railsbetauser OWNER TO app;

--
-- Name: railshosting_railsbetauser_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE railshosting_railsbetauser_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE railshosting_railsbetauser_id_seq OWNER TO app;

--
-- Name: railshosting_railsbetauser_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE railshosting_railsbetauser_id_seq OWNED BY railshosting_railsbetauser.id;


--
-- Name: reversion_revision; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE reversion_revision (
    id integer NOT NULL,
    manager_slug character varying(191) NOT NULL,
    date_created timestamp with time zone NOT NULL,
    comment text NOT NULL,
    user_id integer
);


ALTER TABLE reversion_revision OWNER TO app;

--
-- Name: reversion_revision_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE reversion_revision_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE reversion_revision_id_seq OWNER TO app;

--
-- Name: reversion_revision_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE reversion_revision_id_seq OWNED BY reversion_revision.id;


--
-- Name: reversion_version; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE reversion_version (
    id integer NOT NULL,
    object_id text NOT NULL,
    object_id_int integer,
    format character varying(255) NOT NULL,
    serialized_data text NOT NULL,
    object_repr text NOT NULL,
    content_type_id integer NOT NULL,
    revision_id integer NOT NULL
);


ALTER TABLE reversion_version OWNER TO app;

--
-- Name: reversion_version_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE reversion_version_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE reversion_version_id_seq OWNER TO app;

--
-- Name: reversion_version_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE reversion_version_id_seq OWNED BY reversion_version.id;


--
-- Name: taggit_tag; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE taggit_tag (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    slug character varying(100) NOT NULL
);


ALTER TABLE taggit_tag OWNER TO app;

--
-- Name: taggit_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE taggit_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE taggit_tag_id_seq OWNER TO app;

--
-- Name: taggit_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE taggit_tag_id_seq OWNED BY taggit_tag.id;


--
-- Name: taggit_taggeditem; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE taggit_taggeditem (
    id integer NOT NULL,
    object_id integer NOT NULL,
    content_type_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE taggit_taggeditem OWNER TO app;

--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE taggit_taggeditem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE taggit_taggeditem_id_seq OWNER TO app;

--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE taggit_taggeditem_id_seq OWNED BY taggit_taggeditem.id;


--
-- Name: ungleich_ungleichpage; Type: TABLE; Schema: public; Owner: app; Tablespace: 
--

CREATE TABLE ungleich_ungleichpage (
    id integer NOT NULL,
    extended_object_id integer NOT NULL,
    public_extension_id integer,
    image_id integer
);


ALTER TABLE ungleich_ungleichpage OWNER TO app;

--
-- Name: ungleich_ungleichpage_id_seq; Type: SEQUENCE; Schema: public; Owner: app
--

CREATE SEQUENCE ungleich_ungleichpage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ungleich_ungleichpage_id_seq OWNER TO app;

--
-- Name: ungleich_ungleichpage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: app
--

ALTER SEQUENCE ungleich_ungleichpage_id_seq OWNED BY ungleich_ungleichpage.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_cmsplugin ALTER COLUMN id SET DEFAULT nextval('cms_cmsplugin_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_globalpagepermission ALTER COLUMN id SET DEFAULT nextval('cms_globalpagepermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_globalpagepermission_sites ALTER COLUMN id SET DEFAULT nextval('cms_globalpagepermission_sites_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page ALTER COLUMN id SET DEFAULT nextval('cms_page_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page_placeholders ALTER COLUMN id SET DEFAULT nextval('cms_page_placeholders_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pagepermission ALTER COLUMN id SET DEFAULT nextval('cms_pagepermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_placeholder ALTER COLUMN id SET DEFAULT nextval('cms_placeholder_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_staticplaceholder ALTER COLUMN id SET DEFAULT nextval('cms_staticplaceholder_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_title ALTER COLUMN id SET DEFAULT nextval('cms_title_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_usersettings ALTER COLUMN id SET DEFAULT nextval('cms_usersettings_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_image_thumbnailoption ALTER COLUMN id SET DEFAULT nextval('cmsplugin_filer_image_thumbnailoption_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY digital_glarus_message ALTER COLUMN id SET DEFAULT nextval('digital_glarus_message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_select2_keymap ALTER COLUMN id SET DEFAULT nextval('django_select2_keymap_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin_authors ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_authorentriesplugin_authors_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_blogcategory ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_blogcategory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_blogcategory_translation ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_blogcategory_translation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_categories ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_latestpostsplugin_categories_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_tags ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_latestpostsplugin_tags_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_post_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_categories ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_post_categories_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_sites ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_post_sites_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_translation ALTER COLUMN id SET DEFAULT nextval('djangocms_blog_post_translation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_snippet_snippet ALTER COLUMN id SET DEFAULT nextval('djangocms_snippet_snippet_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY easy_thumbnails_source ALTER COLUMN id SET DEFAULT nextval('easy_thumbnails_source_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY easy_thumbnails_thumbnail ALTER COLUMN id SET DEFAULT nextval('easy_thumbnails_thumbnail_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY easy_thumbnails_thumbnaildimensions ALTER COLUMN id SET DEFAULT nextval('easy_thumbnails_thumbnaildimensions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_clipboard ALTER COLUMN id SET DEFAULT nextval('filer_clipboard_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_clipboarditem ALTER COLUMN id SET DEFAULT nextval('filer_clipboarditem_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_file ALTER COLUMN id SET DEFAULT nextval('filer_file_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folder ALTER COLUMN id SET DEFAULT nextval('filer_folder_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folderpermission ALTER COLUMN id SET DEFAULT nextval('filer_folderpermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY menus_cachekey ALTER COLUMN id SET DEFAULT nextval('menus_cachekey_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY railshosting_railsbetauser ALTER COLUMN id SET DEFAULT nextval('railshosting_railsbetauser_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY reversion_revision ALTER COLUMN id SET DEFAULT nextval('reversion_revision_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY reversion_version ALTER COLUMN id SET DEFAULT nextval('reversion_version_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY taggit_tag ALTER COLUMN id SET DEFAULT nextval('taggit_tag_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY taggit_taggeditem ALTER COLUMN id SET DEFAULT nextval('taggit_taggeditem_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: app
--

ALTER TABLE ONLY ungleich_ungleichpage ALTER COLUMN id SET DEFAULT nextval('ungleich_ungleichpage_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: app
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: app
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: app
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add site	7	add_site
20	Can change site	7	change_site
21	Can delete site	7	delete_site
22	Can add user setting	8	add_usersettings
23	Can change user setting	8	change_usersettings
24	Can delete user setting	8	delete_usersettings
25	Can add placeholder	9	add_placeholder
26	Can change placeholder	9	change_placeholder
27	Can delete placeholder	9	delete_placeholder
28	Can use Structure mode	9	use_structure
29	Can add cms plugin	10	add_cmsplugin
30	Can change cms plugin	10	change_cmsplugin
31	Can delete cms plugin	10	delete_cmsplugin
32	Can add page	11	add_page
33	Can change page	11	change_page
34	Can delete page	11	delete_page
35	Can view page	11	view_page
36	Can publish page	11	publish_page
37	Can edit static placeholders	11	edit_static_placeholder
38	Can add Page global permission	12	add_globalpagepermission
39	Can change Page global permission	12	change_globalpagepermission
40	Can delete Page global permission	12	delete_globalpagepermission
41	Can add Page permission	13	add_pagepermission
42	Can change Page permission	13	change_pagepermission
43	Can delete Page permission	13	delete_pagepermission
44	Can add User (page)	14	add_pageuser
45	Can change User (page)	14	change_pageuser
46	Can delete User (page)	14	delete_pageuser
47	Can add User group (page)	15	add_pageusergroup
48	Can change User group (page)	15	change_pageusergroup
49	Can delete User group (page)	15	delete_pageusergroup
50	Can add title	16	add_title
51	Can change title	16	change_title
52	Can delete title	16	delete_title
53	Can add placeholder reference	17	add_placeholderreference
54	Can change placeholder reference	17	change_placeholderreference
55	Can delete placeholder reference	17	delete_placeholderreference
56	Can add static placeholder	18	add_staticplaceholder
57	Can change static placeholder	18	change_staticplaceholder
58	Can delete static placeholder	18	delete_staticplaceholder
59	Can add alias plugin model	19	add_aliaspluginmodel
60	Can change alias plugin model	19	change_aliaspluginmodel
61	Can delete alias plugin model	19	delete_aliaspluginmodel
62	Can add message	20	add_message
63	Can change message	20	change_message
64	Can delete message	20	delete_message
65	Can add cache key	21	add_cachekey
66	Can change cache key	21	change_cachekey
67	Can delete cache key	21	delete_cachekey
68	Can add flash	22	add_flash
69	Can change flash	22	change_flash
70	Can delete flash	22	delete_flash
71	Can add google map	23	add_googlemap
72	Can change google map	23	change_googlemap
73	Can delete google map	23	delete_googlemap
74	Can add inherit page placeholder	24	add_inheritpageplaceholder
75	Can change inherit page placeholder	24	change_inheritpageplaceholder
76	Can delete inherit page placeholder	24	delete_inheritpageplaceholder
77	Can add link	25	add_link
78	Can change link	25	change_link
79	Can delete link	25	delete_link
80	Can add Snippet	26	add_snippet
81	Can change Snippet	26	change_snippet
82	Can delete Snippet	26	delete_snippet
83	Can add Snippet	27	add_snippetptr
84	Can change Snippet	27	change_snippetptr
85	Can delete Snippet	27	delete_snippetptr
86	Can add teaser	28	add_teaser
87	Can change teaser	28	change_teaser
88	Can delete teaser	28	delete_teaser
89	Can add filer file	29	add_filerfile
90	Can change filer file	29	change_filerfile
91	Can delete filer file	29	delete_filerfile
92	Can add filer folder	30	add_filerfolder
93	Can change filer folder	30	change_filerfolder
94	Can delete filer folder	30	delete_filerfolder
95	Can add filer link plugin	31	add_filerlinkplugin
96	Can change filer link plugin	31	change_filerlinkplugin
97	Can delete filer link plugin	31	delete_filerlinkplugin
98	Can add filer teaser	32	add_filerteaser
99	Can change filer teaser	32	change_filerteaser
100	Can delete filer teaser	32	delete_filerteaser
101	Can add filer video	33	add_filervideo
102	Can change filer video	33	change_filervideo
103	Can delete filer video	33	delete_filervideo
104	Can add revision	34	add_revision
105	Can change revision	34	change_revision
106	Can delete revision	34	delete_revision
107	Can add version	35	add_version
108	Can change version	35	change_version
109	Can delete version	35	delete_version
110	Can add text	36	add_text
111	Can change text	36	change_text
112	Can delete text	36	delete_text
113	Can add Folder	37	add_folder
114	Can change Folder	37	change_folder
115	Can delete Folder	37	delete_folder
116	Can use directory listing	37	can_use_directory_listing
117	Can add folder permission	38	add_folderpermission
118	Can change folder permission	38	change_folderpermission
119	Can delete folder permission	38	delete_folderpermission
120	Can add file	39	add_file
121	Can change file	39	change_file
122	Can delete file	39	delete_file
123	Can add clipboard	40	add_clipboard
124	Can change clipboard	40	change_clipboard
125	Can delete clipboard	40	delete_clipboard
126	Can add clipboard item	41	add_clipboarditem
127	Can change clipboard item	41	change_clipboarditem
128	Can delete clipboard item	41	delete_clipboarditem
129	Can add image	42	add_image
130	Can change image	42	change_image
131	Can delete image	42	delete_image
132	Can add source	43	add_source
133	Can change source	43	change_source
134	Can delete source	43	delete_source
135	Can add thumbnail	44	add_thumbnail
136	Can change thumbnail	44	change_thumbnail
137	Can delete thumbnail	44	delete_thumbnail
138	Can add thumbnail dimensions	45	add_thumbnaildimensions
139	Can change thumbnail dimensions	45	change_thumbnaildimensions
140	Can delete thumbnail dimensions	45	delete_thumbnaildimensions
141	Can add filer image	46	add_filerimage
142	Can change filer image	46	change_filerimage
143	Can delete filer image	46	delete_filerimage
144	Can add thumbnail option	47	add_thumbnailoption
145	Can change thumbnail option	47	change_thumbnailoption
146	Can delete thumbnail option	47	delete_thumbnailoption
147	Can add Tag	48	add_tag
148	Can change Tag	48	change_tag
149	Can delete Tag	48	delete_tag
150	Can add Tagged Item	49	add_taggeditem
151	Can change Tagged Item	49	change_taggeditem
152	Can delete Tagged Item	49	delete_taggeditem
153	Can add key map	50	add_keymap
154	Can change key map	50	change_keymap
155	Can delete key map	50	delete_keymap
156	Can add blog category	52	add_blogcategory
157	Can change blog category	52	change_blogcategory
158	Can delete blog category	52	delete_blogcategory
159	Can add blog article	54	add_post
160	Can change blog article	54	change_post
161	Can delete blog article	54	delete_post
162	Can add latest posts plugin	55	add_latestpostsplugin
163	Can change latest posts plugin	55	change_latestpostsplugin
164	Can delete latest posts plugin	55	delete_latestpostsplugin
165	Can add author entries plugin	56	add_authorentriesplugin
166	Can change author entries plugin	56	change_authorentriesplugin
167	Can delete author entries plugin	56	delete_authorentriesplugin
168	Can add ungleich page	57	add_ungleichpage
169	Can change ungleich page	57	change_ungleichpage
170	Can delete ungleich page	57	delete_ungleichpage
171	Can add rails beta user	58	add_railsbetauser
172	Can change rails beta user	58	change_railsbetauser
173	Can delete rails beta user	58	delete_railsbetauser
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('auth_permission_id_seq', 173, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: app
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$15000$zZnX7j8u6ITX$2pKJPLMWngEfr3l6B9uwFPfnG7voFdTgxjLE5vesSvU=	2015-06-09 09:49:41.878131+02	t	ungleich			info@ungleich.ch	t	t	2015-06-09 09:49:41.878131+02
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: app
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: app
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: cms_aliaspluginmodel; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_aliaspluginmodel (cmsplugin_ptr_id, plugin_id, alias_placeholder_id) FROM stdin;
\.


--
-- Data for Name: cms_cmsplugin; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_cmsplugin (id, "position", language, plugin_type, creation_date, changed_date, parent_id, placeholder_id, depth, numchild, path) FROM stdin;
\.


--
-- Name: cms_cmsplugin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_cmsplugin_id_seq', 1, false);


--
-- Data for Name: cms_globalpagepermission; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_globalpagepermission (id, can_change, can_add, can_delete, can_change_advanced_settings, can_publish, can_change_permissions, can_move_page, can_view, can_recover_page, group_id, user_id) FROM stdin;
\.


--
-- Name: cms_globalpagepermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_globalpagepermission_id_seq', 1, false);


--
-- Data for Name: cms_globalpagepermission_sites; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_globalpagepermission_sites (id, globalpagepermission_id, site_id) FROM stdin;
\.


--
-- Name: cms_globalpagepermission_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_globalpagepermission_sites_id_seq', 1, false);


--
-- Data for Name: cms_page; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_page (id, created_by, changed_by, creation_date, changed_date, publication_date, publication_end_date, in_navigation, soft_root, reverse_id, navigation_extenders, template, login_required, limit_visibility_in_menu, is_home, application_urls, application_namespace, publisher_is_draft, languages, revision_id, xframe_options, parent_id, publisher_public_id, site_id, depth, numchild, path) FROM stdin;
\.


--
-- Name: cms_page_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_page_id_seq', 1, false);


--
-- Data for Name: cms_page_placeholders; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_page_placeholders (id, page_id, placeholder_id) FROM stdin;
\.


--
-- Name: cms_page_placeholders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_page_placeholders_id_seq', 1, false);


--
-- Data for Name: cms_pagepermission; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_pagepermission (id, can_change, can_add, can_delete, can_change_advanced_settings, can_publish, can_change_permissions, can_move_page, can_view, grant_on, group_id, page_id, user_id) FROM stdin;
\.


--
-- Name: cms_pagepermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_pagepermission_id_seq', 1, false);


--
-- Data for Name: cms_pageuser; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_pageuser (user_ptr_id, created_by_id) FROM stdin;
\.


--
-- Data for Name: cms_pageusergroup; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_pageusergroup (group_ptr_id, created_by_id) FROM stdin;
\.


--
-- Data for Name: cms_placeholder; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_placeholder (id, slot, default_width) FROM stdin;
\.


--
-- Name: cms_placeholder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_placeholder_id_seq', 1, false);


--
-- Data for Name: cms_placeholderreference; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_placeholderreference (cmsplugin_ptr_id, name, placeholder_ref_id) FROM stdin;
\.


--
-- Data for Name: cms_staticplaceholder; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_staticplaceholder (id, name, code, dirty, creation_method, draft_id, public_id, site_id) FROM stdin;
\.


--
-- Name: cms_staticplaceholder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_staticplaceholder_id_seq', 1, false);


--
-- Data for Name: cms_title; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_title (id, language, title, page_title, menu_title, meta_description, slug, path, has_url_overwrite, redirect, creation_date, published, publisher_is_draft, publisher_state, page_id, publisher_public_id) FROM stdin;
\.


--
-- Name: cms_title_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_title_id_seq', 1, false);


--
-- Data for Name: cms_usersettings; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cms_usersettings (id, language, clipboard_id, user_id) FROM stdin;
\.


--
-- Name: cms_usersettings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cms_usersettings_id_seq', 1, false);


--
-- Data for Name: cmsplugin_filer_file_filerfile; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_file_filerfile (cmsplugin_ptr_id, title, target_blank, style, file_id) FROM stdin;
\.


--
-- Data for Name: cmsplugin_filer_folder_filerfolder; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_folder_filerfolder (cmsplugin_ptr_id, title, style, folder_id) FROM stdin;
\.


--
-- Data for Name: cmsplugin_filer_image_filerimage; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_image_filerimage (cmsplugin_ptr_id, style, caption_text, image_url, alt_text, use_original_image, use_autoscale, width, height, crop, upscale, alignment, free_link, original_link, description, target_blank, file_link_id, image_id, page_link_id, thumbnail_option_id) FROM stdin;
\.


--
-- Data for Name: cmsplugin_filer_image_thumbnailoption; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_image_thumbnailoption (id, name, width, height, crop, upscale) FROM stdin;
\.


--
-- Name: cmsplugin_filer_image_thumbnailoption_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('cmsplugin_filer_image_thumbnailoption_id_seq', 1, false);


--
-- Data for Name: cmsplugin_filer_link_filerlinkplugin; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_link_filerlinkplugin (cmsplugin_ptr_id, name, url, mailto, link_style, new_window, file_id, page_link_id) FROM stdin;
\.


--
-- Data for Name: cmsplugin_filer_teaser_filerteaser; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_teaser_filerteaser (cmsplugin_ptr_id, title, image_url, style, use_autoscale, width, height, free_link, description, target_blank, image_id, page_link_id) FROM stdin;
\.


--
-- Data for Name: cmsplugin_filer_video_filervideo; Type: TABLE DATA; Schema: public; Owner: app
--

COPY cmsplugin_filer_video_filervideo (cmsplugin_ptr_id, movie_url, width, height, auto_play, auto_hide, fullscreen, loop, bgcolor, textcolor, seekbarcolor, seekbarbgcolor, loadingbarcolor, buttonoutcolor, buttonovercolor, buttonhighlightcolor, image_id, movie_id) FROM stdin;
\.


--
-- Data for Name: digital_glarus_message; Type: TABLE DATA; Schema: public; Owner: app
--

COPY digital_glarus_message (id, name, email, phone_number, message, received_date) FROM stdin;
\.


--
-- Name: digital_glarus_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('digital_glarus_message_id_seq', 1, false);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: app
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, false);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: app
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	log entry	admin	logentry
2	permission	auth	permission
3	group	auth	group
4	user	auth	user
5	content type	contenttypes	contenttype
6	session	sessions	session
7	site	sites	site
8	user setting	cms	usersettings
9	placeholder	cms	placeholder
10	cms plugin	cms	cmsplugin
11	page	cms	page
12	Page global permission	cms	globalpagepermission
13	Page permission	cms	pagepermission
14	User (page)	cms	pageuser
15	User group (page)	cms	pageusergroup
16	title	cms	title
17	placeholder reference	cms	placeholderreference
18	static placeholder	cms	staticplaceholder
19	alias plugin model	cms	aliaspluginmodel
20	message	digital_glarus	message
21	cache key	menus	cachekey
22	flash	djangocms_flash	flash
23	google map	djangocms_googlemap	googlemap
24	inherit page placeholder	djangocms_inherit	inheritpageplaceholder
25	link	djangocms_link	link
26	Snippet	djangocms_snippet	snippet
27	Snippet	djangocms_snippet	snippetptr
28	teaser	djangocms_teaser	teaser
29	filer file	cmsplugin_filer_file	filerfile
30	filer folder	cmsplugin_filer_folder	filerfolder
31	filer link plugin	cmsplugin_filer_link	filerlinkplugin
32	filer teaser	cmsplugin_filer_teaser	filerteaser
33	filer video	cmsplugin_filer_video	filervideo
34	revision	reversion	revision
35	version	reversion	version
36	text	djangocms_text_ckeditor	text
37	Folder	filer	folder
38	folder permission	filer	folderpermission
39	file	filer	file
40	clipboard	filer	clipboard
41	clipboard item	filer	clipboarditem
42	image	filer	image
43	source	easy_thumbnails	source
44	thumbnail	easy_thumbnails	thumbnail
45	thumbnail dimensions	easy_thumbnails	thumbnaildimensions
46	filer image	cmsplugin_filer_image	filerimage
47	thumbnail option	cmsplugin_filer_image	thumbnailoption
48	Tag	taggit	tag
49	Tagged Item	taggit	taggeditem
50	key map	django_select2	keymap
51	blog category Translation	djangocms_blog	blogcategorytranslation
52	blog category	djangocms_blog	blogcategory
53	blog article Translation	djangocms_blog	posttranslation
54	blog article	djangocms_blog	post
55	latest posts plugin	djangocms_blog	latestpostsplugin
56	author entries plugin	djangocms_blog	authorentriesplugin
57	ungleich page	ungleich	ungleichpage
58	rails beta user	railshosting	railsbetauser
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('django_content_type_id_seq', 58, true);


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: app
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2015-06-09 09:48:04.904742+02
2	auth	0001_initial	2015-06-09 09:48:06.128929+02
3	admin	0001_initial	2015-06-09 09:48:06.436316+02
4	sites	0001_initial	2015-06-09 09:48:06.571094+02
5	cms	0001_initial	2015-06-09 09:48:09.53504+02
6	cms	0002_auto_20140816_1918	2015-06-09 09:48:12.559527+02
7	cms	0003_auto_20140926_2347	2015-06-09 09:48:12.733236+02
8	cms	0004_auto_20140924_1038	2015-06-09 09:48:19.378879+02
9	cms	0005_auto_20140924_1039	2015-06-09 09:48:19.537375+02
10	cms	0006_auto_20140924_1110	2015-06-09 09:48:20.251546+02
11	cms	0007_auto_20141028_1559	2015-06-09 09:48:20.545445+02
12	cms	0008_auto_20150208_2149	2015-06-09 09:48:20.824152+02
13	cms	0008_auto_20150121_0059	2015-06-09 09:48:21.219992+02
14	cms	0009_merge	2015-06-09 09:48:21.44872+02
15	cms	0010_migrate_use_structure	2015-06-09 09:48:21.759754+02
16	cms	0011_auto_20150419_1006	2015-06-09 09:48:22.276412+02
17	filer	0001_initial	2015-06-09 09:48:23.993126+02
18	cmsplugin_filer_file	0001_initial	2015-06-09 09:48:24.578561+02
19	cmsplugin_filer_folder	0001_initial	2015-06-09 09:48:25.082482+02
20	cmsplugin_filer_image	0001_initial	2015-06-09 09:48:25.89717+02
21	cmsplugin_filer_link	0001_initial	2015-06-09 09:48:26.375116+02
22	cmsplugin_filer_link	0002_auto_20150609_0744	2015-06-09 09:48:26.613857+02
23	cmsplugin_filer_teaser	0001_initial	2015-06-09 09:48:27.048109+02
24	cmsplugin_filer_video	0001_initial	2015-06-09 09:48:27.515533+02
25	digital_glarus	0001_initial	2015-06-09 09:48:27.798619+02
26	digital_glarus	0002_auto_20150527_1023	2015-06-09 09:48:28.062206+02
27	digital_glarus	0002_auto_20150522_0450	2015-06-09 09:48:28.11565+02
28	digital_glarus	0003_merge	2015-06-09 09:48:28.142738+02
29	taggit	0001_initial	2015-06-09 09:48:28.955569+02
30	djangocms_blog	0001_initial	2015-06-09 09:48:32.72078+02
31	djangocms_blog	0002_post_sites	2015-06-09 09:48:33.508798+02
32	djangocms_blog	0003_auto_20141201_2252	2015-06-09 09:48:33.980756+02
33	djangocms_blog	0004_auto_20150108_1435	2015-06-09 09:48:34.726072+02
34	djangocms_blog	0005_auto_20150212_1118	2015-06-09 09:48:35.382969+02
35	djangocms_blog	0006_auto_20150609_0744	2015-06-09 09:48:36.184509+02
36	djangocms_flash	0001_initial	2015-06-09 09:48:36.432308+02
37	djangocms_googlemap	0001_initial	2015-06-09 09:48:36.790296+02
38	djangocms_inherit	0001_initial	2015-06-09 09:48:36.999143+02
39	djangocms_link	0001_initial	2015-06-09 09:48:37.2923+02
40	djangocms_link	0002_auto_20140929_1705	2015-06-09 09:48:37.398828+02
41	djangocms_link	0003_auto_20150212_1310	2015-06-09 09:48:37.537263+02
42	djangocms_snippet	0001_initial	2015-06-09 09:48:38.079821+02
43	djangocms_teaser	0001_initial	2015-06-09 09:48:38.335323+02
44	djangocms_text_ckeditor	0001_initial	2015-06-09 09:48:38.383933+02
45	easy_thumbnails	0001_initial	2015-06-09 09:48:39.203789+02
46	easy_thumbnails	0002_thumbnaildimensions	2015-06-09 09:48:39.382236+02
47	filer	0002_auto_20150609_0744	2015-06-09 09:48:39.607509+02
48	reversion	0001_initial	2015-06-09 09:48:40.508176+02
49	reversion	0002_auto_20141216_1509	2015-06-09 09:48:41.075416+02
50	sessions	0001_initial	2015-06-09 09:48:41.381849+02
51	ungleich	0001_initial	2015-06-09 09:48:41.874871+02
52	ungleich	0002_ungleichpage_image	2015-06-09 09:48:42.280144+02
53	ungleich	0003_remove_ungleichpage_image_header	2015-06-09 09:48:42.695958+02
\.


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('django_migrations_id_seq', 53, true);


--
-- Data for Name: django_select2_keymap; Type: TABLE DATA; Schema: public; Owner: app
--

COPY django_select2_keymap (id, key, value, accessed_on) FROM stdin;
\.


--
-- Name: django_select2_keymap_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('django_select2_keymap_id_seq', 1, false);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: app
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: app
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Data for Name: djangocms_blog_authorentriesplugin; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_authorentriesplugin (cmsplugin_ptr_id, latest_posts) FROM stdin;
\.


--
-- Data for Name: djangocms_blog_authorentriesplugin_authors; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_authorentriesplugin_authors (id, authorentriesplugin_id, user_id) FROM stdin;
\.


--
-- Name: djangocms_blog_authorentriesplugin_authors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_authorentriesplugin_authors_id_seq', 1, false);


--
-- Data for Name: djangocms_blog_blogcategory; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_blogcategory (id, date_created, date_modified, parent_id) FROM stdin;
\.


--
-- Name: djangocms_blog_blogcategory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_blogcategory_id_seq', 1, false);


--
-- Data for Name: djangocms_blog_blogcategory_translation; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_blogcategory_translation (id, language_code, name, slug, master_id) FROM stdin;
\.


--
-- Name: djangocms_blog_blogcategory_translation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_blogcategory_translation_id_seq', 1, false);


--
-- Data for Name: djangocms_blog_latestpostsplugin; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_latestpostsplugin (cmsplugin_ptr_id, latest_posts) FROM stdin;
\.


--
-- Data for Name: djangocms_blog_latestpostsplugin_categories; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_latestpostsplugin_categories (id, latestpostsplugin_id, blogcategory_id) FROM stdin;
\.


--
-- Name: djangocms_blog_latestpostsplugin_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_latestpostsplugin_categories_id_seq', 1, false);


--
-- Data for Name: djangocms_blog_latestpostsplugin_tags; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_latestpostsplugin_tags (id, latestpostsplugin_id, tag_id) FROM stdin;
\.


--
-- Name: djangocms_blog_latestpostsplugin_tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_latestpostsplugin_tags_id_seq', 1, false);


--
-- Data for Name: djangocms_blog_post; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_post (id, date_created, date_modified, date_published, date_published_end, publish, enable_comments, author_id, content_id, main_image_id, main_image_full_id, main_image_thumbnail_id) FROM stdin;
\.


--
-- Data for Name: djangocms_blog_post_categories; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_post_categories (id, post_id, blogcategory_id) FROM stdin;
\.


--
-- Name: djangocms_blog_post_categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_post_categories_id_seq', 1, false);


--
-- Name: djangocms_blog_post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_post_id_seq', 1, false);


--
-- Data for Name: djangocms_blog_post_sites; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_post_sites (id, post_id, site_id) FROM stdin;
\.


--
-- Name: djangocms_blog_post_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_post_sites_id_seq', 1, false);


--
-- Data for Name: djangocms_blog_post_translation; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_blog_post_translation (id, language_code, title, slug, abstract, meta_description, meta_keywords, meta_title, post_text, master_id) FROM stdin;
\.


--
-- Name: djangocms_blog_post_translation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_blog_post_translation_id_seq', 1, false);


--
-- Data for Name: djangocms_flash_flash; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_flash_flash (cmsplugin_ptr_id, file, width, height) FROM stdin;
\.


--
-- Data for Name: djangocms_googlemap_googlemap; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_googlemap_googlemap (cmsplugin_ptr_id, title, address, zipcode, city, content, zoom, lat, lng, route_planer_title, route_planer, width, height, info_window, scrollwheel, double_click_zoom, draggable, keyboard_shortcuts, pan_control, zoom_control, street_view_control) FROM stdin;
\.


--
-- Data for Name: djangocms_inherit_inheritpageplaceholder; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_inherit_inheritpageplaceholder (cmsplugin_ptr_id, from_language, from_page_id) FROM stdin;
\.


--
-- Data for Name: djangocms_link_link; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_link_link (cmsplugin_ptr_id, name, url, anchor, mailto, phone, target, page_link_id) FROM stdin;
\.


--
-- Data for Name: djangocms_snippet_snippet; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_snippet_snippet (id, name, html, template) FROM stdin;
\.


--
-- Name: djangocms_snippet_snippet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('djangocms_snippet_snippet_id_seq', 1, false);


--
-- Data for Name: djangocms_snippet_snippetptr; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_snippet_snippetptr (cmsplugin_ptr_id, snippet_id) FROM stdin;
\.


--
-- Data for Name: djangocms_teaser_teaser; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_teaser_teaser (cmsplugin_ptr_id, title, image, url, description, page_link_id) FROM stdin;
\.


--
-- Data for Name: djangocms_text_ckeditor_text; Type: TABLE DATA; Schema: public; Owner: app
--

COPY djangocms_text_ckeditor_text (cmsplugin_ptr_id, body) FROM stdin;
\.


--
-- Data for Name: easy_thumbnails_source; Type: TABLE DATA; Schema: public; Owner: app
--

COPY easy_thumbnails_source (id, storage_hash, name, modified) FROM stdin;
\.


--
-- Name: easy_thumbnails_source_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('easy_thumbnails_source_id_seq', 1, false);


--
-- Data for Name: easy_thumbnails_thumbnail; Type: TABLE DATA; Schema: public; Owner: app
--

COPY easy_thumbnails_thumbnail (id, storage_hash, name, modified, source_id) FROM stdin;
\.


--
-- Name: easy_thumbnails_thumbnail_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('easy_thumbnails_thumbnail_id_seq', 1, false);


--
-- Data for Name: easy_thumbnails_thumbnaildimensions; Type: TABLE DATA; Schema: public; Owner: app
--

COPY easy_thumbnails_thumbnaildimensions (id, thumbnail_id, width, height) FROM stdin;
\.


--
-- Name: easy_thumbnails_thumbnaildimensions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('easy_thumbnails_thumbnaildimensions_id_seq', 1, false);


--
-- Data for Name: filer_clipboard; Type: TABLE DATA; Schema: public; Owner: app
--

COPY filer_clipboard (id, user_id) FROM stdin;
\.


--
-- Name: filer_clipboard_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('filer_clipboard_id_seq', 1, false);


--
-- Data for Name: filer_clipboarditem; Type: TABLE DATA; Schema: public; Owner: app
--

COPY filer_clipboarditem (id, clipboard_id, file_id) FROM stdin;
\.


--
-- Name: filer_clipboarditem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('filer_clipboarditem_id_seq', 1, false);


--
-- Data for Name: filer_file; Type: TABLE DATA; Schema: public; Owner: app
--

COPY filer_file (id, file, _file_size, sha1, has_all_mandatory_data, original_filename, name, description, uploaded_at, modified_at, is_public, folder_id, owner_id, polymorphic_ctype_id) FROM stdin;
\.


--
-- Name: filer_file_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('filer_file_id_seq', 1, false);


--
-- Data for Name: filer_folder; Type: TABLE DATA; Schema: public; Owner: app
--

COPY filer_folder (id, name, uploaded_at, created_at, modified_at, lft, rght, tree_id, level, owner_id, parent_id) FROM stdin;
\.


--
-- Name: filer_folder_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('filer_folder_id_seq', 1, false);


--
-- Data for Name: filer_folderpermission; Type: TABLE DATA; Schema: public; Owner: app
--

COPY filer_folderpermission (id, type, everybody, can_edit, can_read, can_add_children, folder_id, group_id, user_id) FROM stdin;
\.


--
-- Name: filer_folderpermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('filer_folderpermission_id_seq', 1, false);


--
-- Data for Name: filer_image; Type: TABLE DATA; Schema: public; Owner: app
--

COPY filer_image (file_ptr_id, _height, _width, date_taken, default_alt_text, default_caption, author, must_always_publish_author_credit, must_always_publish_copyright, subject_location) FROM stdin;
\.


--
-- Data for Name: menus_cachekey; Type: TABLE DATA; Schema: public; Owner: app
--

COPY menus_cachekey (id, language, site, key) FROM stdin;
\.


--
-- Name: menus_cachekey_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('menus_cachekey_id_seq', 1, false);


--
-- Data for Name: railshosting_railsbetauser; Type: TABLE DATA; Schema: public; Owner: app
--

COPY railshosting_railsbetauser (id, email, received_date) FROM stdin;
\.


--
-- Name: railshosting_railsbetauser_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('railshosting_railsbetauser_id_seq', 1, false);


--
-- Data for Name: reversion_revision; Type: TABLE DATA; Schema: public; Owner: app
--

COPY reversion_revision (id, manager_slug, date_created, comment, user_id) FROM stdin;
\.


--
-- Name: reversion_revision_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('reversion_revision_id_seq', 1, false);


--
-- Data for Name: reversion_version; Type: TABLE DATA; Schema: public; Owner: app
--

COPY reversion_version (id, object_id, object_id_int, format, serialized_data, object_repr, content_type_id, revision_id) FROM stdin;
\.


--
-- Name: reversion_version_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('reversion_version_id_seq', 1, false);


--
-- Data for Name: taggit_tag; Type: TABLE DATA; Schema: public; Owner: app
--

COPY taggit_tag (id, name, slug) FROM stdin;
\.


--
-- Name: taggit_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('taggit_tag_id_seq', 1, false);


--
-- Data for Name: taggit_taggeditem; Type: TABLE DATA; Schema: public; Owner: app
--

COPY taggit_taggeditem (id, object_id, content_type_id, tag_id) FROM stdin;
\.


--
-- Name: taggit_taggeditem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('taggit_taggeditem_id_seq', 1, false);


--
-- Data for Name: ungleich_ungleichpage; Type: TABLE DATA; Schema: public; Owner: app
--

COPY ungleich_ungleichpage (id, extended_object_id, public_extension_id, image_id) FROM stdin;
\.


--
-- Name: ungleich_ungleichpage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: app
--

SELECT pg_catalog.setval('ungleich_ungleichpage_id_seq', 1, false);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: cms_aliaspluginmodel_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_aliaspluginmodel
    ADD CONSTRAINT cms_aliaspluginmodel_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cms_cmsplugin_path_5e1f7519553fd38c_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmsplugin_path_5e1f7519553fd38c_uniq UNIQUE (path);


--
-- Name: cms_cmsplugin_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmsplugin_pkey PRIMARY KEY (id);


--
-- Name: cms_globalpagepermission_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_globalpagepermission
    ADD CONSTRAINT cms_globalpagepermission_pkey PRIMARY KEY (id);


--
-- Name: cms_globalpagepermission_site_globalpagepermission_id_site__key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_globalpagepermission_sites
    ADD CONSTRAINT cms_globalpagepermission_site_globalpagepermission_id_site__key UNIQUE (globalpagepermission_id, site_id);


--
-- Name: cms_globalpagepermission_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_globalpagepermission_sites
    ADD CONSTRAINT cms_globalpagepermission_sites_pkey PRIMARY KEY (id);


--
-- Name: cms_page_path_379b7cdb14a777d0_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_path_379b7cdb14a777d0_uniq UNIQUE (path);


--
-- Name: cms_page_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_pkey PRIMARY KEY (id);


--
-- Name: cms_page_placeholders_page_id_placeholder_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page_placeholders
    ADD CONSTRAINT cms_page_placeholders_page_id_placeholder_id_key UNIQUE (page_id, placeholder_id);


--
-- Name: cms_page_placeholders_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page_placeholders
    ADD CONSTRAINT cms_page_placeholders_pkey PRIMARY KEY (id);


--
-- Name: cms_page_publisher_is_draft_4691bdc0393fad7e_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_publisher_is_draft_4691bdc0393fad7e_uniq UNIQUE (publisher_is_draft, site_id, application_namespace);


--
-- Name: cms_page_publisher_public_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_publisher_public_id_key UNIQUE (publisher_public_id);


--
-- Name: cms_page_reverse_id_7163ce188d981c94_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_reverse_id_7163ce188d981c94_uniq UNIQUE (reverse_id, site_id, publisher_is_draft);


--
-- Name: cms_pagepermission_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_pagepermission
    ADD CONSTRAINT cms_pagepermission_pkey PRIMARY KEY (id);


--
-- Name: cms_pageuser_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_pageuser
    ADD CONSTRAINT cms_pageuser_pkey PRIMARY KEY (user_ptr_id);


--
-- Name: cms_pageusergroup_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_pageusergroup
    ADD CONSTRAINT cms_pageusergroup_pkey PRIMARY KEY (group_ptr_id);


--
-- Name: cms_placeholder_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_placeholder
    ADD CONSTRAINT cms_placeholder_pkey PRIMARY KEY (id);


--
-- Name: cms_placeholderreference_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_placeholderreference
    ADD CONSTRAINT cms_placeholderreference_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cms_staticplaceholder_code_3f781b18db4d3da1_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplaceholder_code_3f781b18db4d3da1_uniq UNIQUE (code, site_id);


--
-- Name: cms_staticplaceholder_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplaceholder_pkey PRIMARY KEY (id);


--
-- Name: cms_title_language_78eb9650320816de_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_language_78eb9650320816de_uniq UNIQUE (language, page_id);


--
-- Name: cms_title_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_pkey PRIMARY KEY (id);


--
-- Name: cms_title_publisher_public_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_publisher_public_id_key UNIQUE (publisher_public_id);


--
-- Name: cms_usersettings_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_usersettings
    ADD CONSTRAINT cms_usersettings_pkey PRIMARY KEY (id);


--
-- Name: cms_usersettings_user_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cms_usersettings
    ADD CONSTRAINT cms_usersettings_user_id_key UNIQUE (user_id);


--
-- Name: cmsplugin_filer_file_filerfile_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_file_filerfile
    ADD CONSTRAINT cmsplugin_filer_file_filerfile_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cmsplugin_filer_folder_filerfolder_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_folder_filerfolder
    ADD CONSTRAINT cmsplugin_filer_folder_filerfolder_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cmsplugin_filer_image_filerimage_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_image_filerimage
    ADD CONSTRAINT cmsplugin_filer_image_filerimage_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cmsplugin_filer_image_thumbnailoption_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_image_thumbnailoption
    ADD CONSTRAINT cmsplugin_filer_image_thumbnailoption_pkey PRIMARY KEY (id);


--
-- Name: cmsplugin_filer_link_filerlinkplugin_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_link_filerlinkplugin
    ADD CONSTRAINT cmsplugin_filer_link_filerlinkplugin_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cmsplugin_filer_teaser_filerteaser_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_teaser_filerteaser
    ADD CONSTRAINT cmsplugin_filer_teaser_filerteaser_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: cmsplugin_filer_video_filervideo_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY cmsplugin_filer_video_filervideo
    ADD CONSTRAINT cmsplugin_filer_video_filervideo_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: digital_glarus_message_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY digital_glarus_message
    ADD CONSTRAINT digital_glarus_message_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_6c0fb2aa9d6a702d_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_6c0fb2aa9d6a702d_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_select2_keymap_key_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_select2_keymap
    ADD CONSTRAINT django_select2_keymap_key_key UNIQUE (key);


--
-- Name: django_select2_keymap_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_select2_keymap
    ADD CONSTRAINT django_select2_keymap_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_authorentriesp_authorentriesplugin_id_user_i_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin_authors
    ADD CONSTRAINT djangocms_blog_authorentriesp_authorentriesplugin_id_user_i_key UNIQUE (authorentriesplugin_id, user_id);


--
-- Name: djangocms_blog_authorentriesplugin_authors_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin_authors
    ADD CONSTRAINT djangocms_blog_authorentriesplugin_authors_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_authorentriesplugin_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin
    ADD CONSTRAINT djangocms_blog_authorentriesplugin_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_blog_blogcategory_language_code_5c2df89f0f117750_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_blogcategory_translation
    ADD CONSTRAINT djangocms_blog_blogcategory_language_code_5c2df89f0f117750_uniq UNIQUE (language_code, master_id);


--
-- Name: djangocms_blog_blogcategory_language_code_650aa1d5d9e83b8e_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_blogcategory_translation
    ADD CONSTRAINT djangocms_blog_blogcategory_language_code_650aa1d5d9e83b8e_uniq UNIQUE (language_code, slug);


--
-- Name: djangocms_blog_blogcategory_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_blogcategory
    ADD CONSTRAINT djangocms_blog_blogcategory_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_blogcategory_translation_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_blogcategory_translation
    ADD CONSTRAINT djangocms_blog_blogcategory_translation_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_latestpostsplu_latestpostsplugin_id_blogcate_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_categories
    ADD CONSTRAINT djangocms_blog_latestpostsplu_latestpostsplugin_id_blogcate_key UNIQUE (latestpostsplugin_id, blogcategory_id);


--
-- Name: djangocms_blog_latestpostsplugi_latestpostsplugin_id_tag_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_tags
    ADD CONSTRAINT djangocms_blog_latestpostsplugi_latestpostsplugin_id_tag_id_key UNIQUE (latestpostsplugin_id, tag_id);


--
-- Name: djangocms_blog_latestpostsplugin_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_categories
    ADD CONSTRAINT djangocms_blog_latestpostsplugin_categories_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_latestpostsplugin_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin
    ADD CONSTRAINT djangocms_blog_latestpostsplugin_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_blog_latestpostsplugin_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_tags
    ADD CONSTRAINT djangocms_blog_latestpostsplugin_tags_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_post_categories_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_categories
    ADD CONSTRAINT djangocms_blog_post_categories_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_post_categories_post_id_blogcategory_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_categories
    ADD CONSTRAINT djangocms_blog_post_categories_post_id_blogcategory_id_key UNIQUE (post_id, blogcategory_id);


--
-- Name: djangocms_blog_post_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post
    ADD CONSTRAINT djangocms_blog_post_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_post_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_sites
    ADD CONSTRAINT djangocms_blog_post_sites_pkey PRIMARY KEY (id);


--
-- Name: djangocms_blog_post_sites_post_id_site_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_sites
    ADD CONSTRAINT djangocms_blog_post_sites_post_id_site_id_key UNIQUE (post_id, site_id);


--
-- Name: djangocms_blog_post_transla_language_code_1f72994b5955fdcc_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_translation
    ADD CONSTRAINT djangocms_blog_post_transla_language_code_1f72994b5955fdcc_uniq UNIQUE (language_code, master_id);


--
-- Name: djangocms_blog_post_transla_language_code_3179d6f84bb95dca_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_translation
    ADD CONSTRAINT djangocms_blog_post_transla_language_code_3179d6f84bb95dca_uniq UNIQUE (language_code, slug);


--
-- Name: djangocms_blog_post_translation_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_blog_post_translation
    ADD CONSTRAINT djangocms_blog_post_translation_pkey PRIMARY KEY (id);


--
-- Name: djangocms_flash_flash_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_flash_flash
    ADD CONSTRAINT djangocms_flash_flash_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_googlemap_googlemap_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_googlemap_googlemap
    ADD CONSTRAINT djangocms_googlemap_googlemap_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_inherit_inheritpageplaceholder_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_inherit_inheritpageplaceholder
    ADD CONSTRAINT djangocms_inherit_inheritpageplaceholder_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_link_link_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_link_link
    ADD CONSTRAINT djangocms_link_link_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_snippet_snippet_name_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_snippet_snippet
    ADD CONSTRAINT djangocms_snippet_snippet_name_key UNIQUE (name);


--
-- Name: djangocms_snippet_snippet_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_snippet_snippet
    ADD CONSTRAINT djangocms_snippet_snippet_pkey PRIMARY KEY (id);


--
-- Name: djangocms_snippet_snippetptr_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_snippet_snippetptr
    ADD CONSTRAINT djangocms_snippet_snippetptr_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_teaser_teaser_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_teaser_teaser
    ADD CONSTRAINT djangocms_teaser_teaser_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: djangocms_text_ckeditor_text_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY djangocms_text_ckeditor_text
    ADD CONSTRAINT djangocms_text_ckeditor_text_pkey PRIMARY KEY (cmsplugin_ptr_id);


--
-- Name: easy_thumbnails_source_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY easy_thumbnails_source
    ADD CONSTRAINT easy_thumbnails_source_pkey PRIMARY KEY (id);


--
-- Name: easy_thumbnails_source_storage_hash_765547776e36d1ad_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY easy_thumbnails_source
    ADD CONSTRAINT easy_thumbnails_source_storage_hash_765547776e36d1ad_uniq UNIQUE (storage_hash, name);


--
-- Name: easy_thumbnails_thumbnail_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY easy_thumbnails_thumbnail
    ADD CONSTRAINT easy_thumbnails_thumbnail_pkey PRIMARY KEY (id);


--
-- Name: easy_thumbnails_thumbnail_storage_hash_2936071d7ec413f8_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY easy_thumbnails_thumbnail
    ADD CONSTRAINT easy_thumbnails_thumbnail_storage_hash_2936071d7ec413f8_uniq UNIQUE (storage_hash, name, source_id);


--
-- Name: easy_thumbnails_thumbnaildimensions_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY easy_thumbnails_thumbnaildimensions
    ADD CONSTRAINT easy_thumbnails_thumbnaildimensions_pkey PRIMARY KEY (id);


--
-- Name: easy_thumbnails_thumbnaildimensions_thumbnail_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY easy_thumbnails_thumbnaildimensions
    ADD CONSTRAINT easy_thumbnails_thumbnaildimensions_thumbnail_id_key UNIQUE (thumbnail_id);


--
-- Name: filer_clipboard_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_clipboard
    ADD CONSTRAINT filer_clipboard_pkey PRIMARY KEY (id);


--
-- Name: filer_clipboarditem_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_clipboarditem
    ADD CONSTRAINT filer_clipboarditem_pkey PRIMARY KEY (id);


--
-- Name: filer_file_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_file
    ADD CONSTRAINT filer_file_pkey PRIMARY KEY (id);


--
-- Name: filer_folder_parent_id_3be3c11ed42108_uniq; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_folder
    ADD CONSTRAINT filer_folder_parent_id_3be3c11ed42108_uniq UNIQUE (parent_id, name);


--
-- Name: filer_folder_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_folder
    ADD CONSTRAINT filer_folder_pkey PRIMARY KEY (id);


--
-- Name: filer_folderpermission_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_folderpermission
    ADD CONSTRAINT filer_folderpermission_pkey PRIMARY KEY (id);


--
-- Name: filer_image_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY filer_image
    ADD CONSTRAINT filer_image_pkey PRIMARY KEY (file_ptr_id);


--
-- Name: menus_cachekey_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY menus_cachekey
    ADD CONSTRAINT menus_cachekey_pkey PRIMARY KEY (id);


--
-- Name: railshosting_railsbetauser_email_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY railshosting_railsbetauser
    ADD CONSTRAINT railshosting_railsbetauser_email_key UNIQUE (email);


--
-- Name: railshosting_railsbetauser_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY railshosting_railsbetauser
    ADD CONSTRAINT railshosting_railsbetauser_pkey PRIMARY KEY (id);


--
-- Name: reversion_revision_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY reversion_revision
    ADD CONSTRAINT reversion_revision_pkey PRIMARY KEY (id);


--
-- Name: reversion_version_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY reversion_version
    ADD CONSTRAINT reversion_version_pkey PRIMARY KEY (id);


--
-- Name: taggit_tag_name_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_name_key UNIQUE (name);


--
-- Name: taggit_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_pkey PRIMARY KEY (id);


--
-- Name: taggit_tag_slug_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY taggit_tag
    ADD CONSTRAINT taggit_tag_slug_key UNIQUE (slug);


--
-- Name: taggit_taggeditem_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_pkey PRIMARY KEY (id);


--
-- Name: ungleich_ungleichpage_extended_object_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY ungleich_ungleichpage
    ADD CONSTRAINT ungleich_ungleichpage_extended_object_id_key UNIQUE (extended_object_id);


--
-- Name: ungleich_ungleichpage_pkey; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY ungleich_ungleichpage
    ADD CONSTRAINT ungleich_ungleichpage_pkey PRIMARY KEY (id);


--
-- Name: ungleich_ungleichpage_public_extension_id_key; Type: CONSTRAINT; Schema: public; Owner: app; Tablespace: 
--

ALTER TABLE ONLY ungleich_ungleichpage
    ADD CONSTRAINT ungleich_ungleichpage_public_extension_id_key UNIQUE (public_extension_id);


--
-- Name: auth_group_name_5df6d188de02deca_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_group_name_5df6d188de02deca_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_0e939a4f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_group_permissions_0e939a4f ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_8373b171; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_group_permissions_8373b171 ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_417f1b1c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_permission_417f1b1c ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_0e939a4f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_user_groups_0e939a4f ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_user_groups_e8701ad4 ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_8373b171; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_8373b171 ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_e8701ad4 ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_3865c2f3a012f65e_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX auth_user_username_3865c2f3a012f65e_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: cms_aliaspluginmodel_921abf5c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_aliaspluginmodel_921abf5c ON cms_aliaspluginmodel USING btree (alias_placeholder_id);


--
-- Name: cms_aliaspluginmodel_b25eaab4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_aliaspluginmodel_b25eaab4 ON cms_aliaspluginmodel USING btree (plugin_id);


--
-- Name: cms_cmsplugin_667a6151; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_cmsplugin_667a6151 ON cms_cmsplugin USING btree (placeholder_id);


--
-- Name: cms_cmsplugin_6be37982; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_cmsplugin_6be37982 ON cms_cmsplugin USING btree (parent_id);


--
-- Name: cms_cmsplugin_8512ae7d; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_cmsplugin_8512ae7d ON cms_cmsplugin USING btree (language);


--
-- Name: cms_cmsplugin_b5e4cf8f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_cmsplugin_b5e4cf8f ON cms_cmsplugin USING btree (plugin_type);


--
-- Name: cms_cmsplugin_language_54f9cbf3b21c8366_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_cmsplugin_language_54f9cbf3b21c8366_like ON cms_cmsplugin USING btree (language varchar_pattern_ops);


--
-- Name: cms_cmsplugin_plugin_type_51184b61128af8fc_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_cmsplugin_plugin_type_51184b61128af8fc_like ON cms_cmsplugin USING btree (plugin_type varchar_pattern_ops);


--
-- Name: cms_globalpagepermission_0e939a4f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_globalpagepermission_0e939a4f ON cms_globalpagepermission USING btree (group_id);


--
-- Name: cms_globalpagepermission_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_globalpagepermission_e8701ad4 ON cms_globalpagepermission USING btree (user_id);


--
-- Name: cms_globalpagepermission_sites_9365d6e7; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_globalpagepermission_sites_9365d6e7 ON cms_globalpagepermission_sites USING btree (site_id);


--
-- Name: cms_globalpagepermission_sites_a3d12ecd; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_globalpagepermission_sites_a3d12ecd ON cms_globalpagepermission_sites USING btree (globalpagepermission_id);


--
-- Name: cms_page_1d85575d; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_1d85575d ON cms_page USING btree (soft_root);


--
-- Name: cms_page_2247c5f0; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_2247c5f0 ON cms_page USING btree (publication_end_date);


--
-- Name: cms_page_3d9ef52f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_3d9ef52f ON cms_page USING btree (reverse_id);


--
-- Name: cms_page_4fa1c803; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_4fa1c803 ON cms_page USING btree (is_home);


--
-- Name: cms_page_6be37982; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_6be37982 ON cms_page USING btree (parent_id);


--
-- Name: cms_page_7b8acfa6; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_7b8acfa6 ON cms_page USING btree (navigation_extenders);


--
-- Name: cms_page_9365d6e7; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_9365d6e7 ON cms_page USING btree (site_id);


--
-- Name: cms_page_93b83098; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_93b83098 ON cms_page USING btree (publication_date);


--
-- Name: cms_page_application_urls_617f6cd17f3aec95_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_application_urls_617f6cd17f3aec95_like ON cms_page USING btree (application_urls varchar_pattern_ops);


--
-- Name: cms_page_b7700099; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_b7700099 ON cms_page USING btree (publisher_is_draft);


--
-- Name: cms_page_cb540373; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_cb540373 ON cms_page USING btree (limit_visibility_in_menu);


--
-- Name: cms_page_db3eb53f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_db3eb53f ON cms_page USING btree (in_navigation);


--
-- Name: cms_page_e721871e; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_e721871e ON cms_page USING btree (application_urls);


--
-- Name: cms_page_navigation_extenders_24a15b533f085cfe_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_navigation_extenders_24a15b533f085cfe_like ON cms_page USING btree (navigation_extenders varchar_pattern_ops);


--
-- Name: cms_page_placeholders_1a63c800; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_placeholders_1a63c800 ON cms_page_placeholders USING btree (page_id);


--
-- Name: cms_page_placeholders_667a6151; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_placeholders_667a6151 ON cms_page_placeholders USING btree (placeholder_id);


--
-- Name: cms_page_reverse_id_440cddee3b829c43_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_page_reverse_id_440cddee3b829c43_like ON cms_page USING btree (reverse_id varchar_pattern_ops);


--
-- Name: cms_pagepermission_0e939a4f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_pagepermission_0e939a4f ON cms_pagepermission USING btree (group_id);


--
-- Name: cms_pagepermission_1a63c800; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_pagepermission_1a63c800 ON cms_pagepermission USING btree (page_id);


--
-- Name: cms_pagepermission_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_pagepermission_e8701ad4 ON cms_pagepermission USING btree (user_id);


--
-- Name: cms_pageuser_e93cb7eb; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_pageuser_e93cb7eb ON cms_pageuser USING btree (created_by_id);


--
-- Name: cms_pageusergroup_e93cb7eb; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_pageusergroup_e93cb7eb ON cms_pageusergroup USING btree (created_by_id);


--
-- Name: cms_placeholder_5e97994e; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_placeholder_5e97994e ON cms_placeholder USING btree (slot);


--
-- Name: cms_placeholder_slot_18c7f524f8cf1b8b_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_placeholder_slot_18c7f524f8cf1b8b_like ON cms_placeholder USING btree (slot varchar_pattern_ops);


--
-- Name: cms_placeholderreference_328d0afc; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_placeholderreference_328d0afc ON cms_placeholderreference USING btree (placeholder_ref_id);


--
-- Name: cms_staticplaceholder_1ee2744d; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_staticplaceholder_1ee2744d ON cms_staticplaceholder USING btree (public_id);


--
-- Name: cms_staticplaceholder_5cb48773; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_staticplaceholder_5cb48773 ON cms_staticplaceholder USING btree (draft_id);


--
-- Name: cms_staticplaceholder_9365d6e7; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_staticplaceholder_9365d6e7 ON cms_staticplaceholder USING btree (site_id);


--
-- Name: cms_title_1268de9a; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_1268de9a ON cms_title USING btree (has_url_overwrite);


--
-- Name: cms_title_1a63c800; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_1a63c800 ON cms_title USING btree (page_id);


--
-- Name: cms_title_2dbcba41; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_2dbcba41 ON cms_title USING btree (slug);


--
-- Name: cms_title_8512ae7d; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_8512ae7d ON cms_title USING btree (language);


--
-- Name: cms_title_b7700099; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_b7700099 ON cms_title USING btree (publisher_is_draft);


--
-- Name: cms_title_d6fe1d0b; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_d6fe1d0b ON cms_title USING btree (path);


--
-- Name: cms_title_f7202fc0; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_f7202fc0 ON cms_title USING btree (publisher_state);


--
-- Name: cms_title_language_319afce44255a674_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_language_319afce44255a674_like ON cms_title USING btree (language varchar_pattern_ops);


--
-- Name: cms_title_path_3e691ba4741b35b2_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_path_3e691ba4741b35b2_like ON cms_title USING btree (path varchar_pattern_ops);


--
-- Name: cms_title_slug_615cef857866903b_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_title_slug_615cef857866903b_like ON cms_title USING btree (slug varchar_pattern_ops);


--
-- Name: cms_usersettings_2655b062; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cms_usersettings_2655b062 ON cms_usersettings USING btree (clipboard_id);


--
-- Name: cmsplugin_filer_file_filerfile_814552b9; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_file_filerfile_814552b9 ON cmsplugin_filer_file_filerfile USING btree (file_id);


--
-- Name: cmsplugin_filer_folder_filerfolder_a8a44dbb; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_folder_filerfolder_a8a44dbb ON cmsplugin_filer_folder_filerfolder USING btree (folder_id);


--
-- Name: cmsplugin_filer_image_filerimage_0fe0fc57; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_image_filerimage_0fe0fc57 ON cmsplugin_filer_image_filerimage USING btree (file_link_id);


--
-- Name: cmsplugin_filer_image_filerimage_6b85b7b1; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_image_filerimage_6b85b7b1 ON cmsplugin_filer_image_filerimage USING btree (thumbnail_option_id);


--
-- Name: cmsplugin_filer_image_filerimage_d916d256; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_image_filerimage_d916d256 ON cmsplugin_filer_image_filerimage USING btree (page_link_id);


--
-- Name: cmsplugin_filer_image_filerimage_f33175e6; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_image_filerimage_f33175e6 ON cmsplugin_filer_image_filerimage USING btree (image_id);


--
-- Name: cmsplugin_filer_link_filerlinkplugin_814552b9; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_link_filerlinkplugin_814552b9 ON cmsplugin_filer_link_filerlinkplugin USING btree (file_id);


--
-- Name: cmsplugin_filer_link_filerlinkplugin_d916d256; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_link_filerlinkplugin_d916d256 ON cmsplugin_filer_link_filerlinkplugin USING btree (page_link_id);


--
-- Name: cmsplugin_filer_teaser_filerteaser_d916d256; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_teaser_filerteaser_d916d256 ON cmsplugin_filer_teaser_filerteaser USING btree (page_link_id);


--
-- Name: cmsplugin_filer_teaser_filerteaser_f33175e6; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_teaser_filerteaser_f33175e6 ON cmsplugin_filer_teaser_filerteaser USING btree (image_id);


--
-- Name: cmsplugin_filer_video_filervideo_d1b173c8; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_video_filervideo_d1b173c8 ON cmsplugin_filer_video_filervideo USING btree (movie_id);


--
-- Name: cmsplugin_filer_video_filervideo_f33175e6; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX cmsplugin_filer_video_filervideo_f33175e6 ON cmsplugin_filer_video_filervideo USING btree (image_id);


--
-- Name: django_admin_log_417f1b1c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX django_admin_log_417f1b1c ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX django_admin_log_e8701ad4 ON django_admin_log USING btree (user_id);


--
-- Name: django_select2_keymap_key_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX django_select2_keymap_key_like ON django_select2_keymap USING btree (key varchar_pattern_ops);


--
-- Name: django_session_de54fa62; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX django_session_de54fa62 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_6beefb891d17bf09_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX django_session_session_key_6beefb891d17bf09_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: djangocms_blog_authorentriesplugin_authors_793c8338; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_authorentriesplugin_authors_793c8338 ON djangocms_blog_authorentriesplugin_authors USING btree (authorentriesplugin_id);


--
-- Name: djangocms_blog_authorentriesplugin_authors_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_authorentriesplugin_authors_e8701ad4 ON djangocms_blog_authorentriesplugin_authors USING btree (user_id);


--
-- Name: djangocms_blog_blogcategory_6be37982; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_blogcategory_6be37982 ON djangocms_blog_blogcategory USING btree (parent_id);


--
-- Name: djangocms_blog_blogcategory_language_code_1f54e0c6383b5af8_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_blogcategory_language_code_1f54e0c6383b5af8_like ON djangocms_blog_blogcategory_translation USING btree (language_code varchar_pattern_ops);


--
-- Name: djangocms_blog_blogcategory_translat_slug_41607e362e74f9e3_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_blogcategory_translat_slug_41607e362e74f9e3_like ON djangocms_blog_blogcategory_translation USING btree (slug varchar_pattern_ops);


--
-- Name: djangocms_blog_blogcategory_translation_2dbcba41; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_blogcategory_translation_2dbcba41 ON djangocms_blog_blogcategory_translation USING btree (slug);


--
-- Name: djangocms_blog_blogcategory_translation_60716c2f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_blogcategory_translation_60716c2f ON djangocms_blog_blogcategory_translation USING btree (language_code);


--
-- Name: djangocms_blog_blogcategory_translation_90349b61; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_blogcategory_translation_90349b61 ON djangocms_blog_blogcategory_translation USING btree (master_id);


--
-- Name: djangocms_blog_latestpostsplugin_categories_efb54956; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_latestpostsplugin_categories_efb54956 ON djangocms_blog_latestpostsplugin_categories USING btree (blogcategory_id);


--
-- Name: djangocms_blog_latestpostsplugin_categories_fda89e10; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_latestpostsplugin_categories_fda89e10 ON djangocms_blog_latestpostsplugin_categories USING btree (latestpostsplugin_id);


--
-- Name: djangocms_blog_latestpostsplugin_tags_76f094bc; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_latestpostsplugin_tags_76f094bc ON djangocms_blog_latestpostsplugin_tags USING btree (tag_id);


--
-- Name: djangocms_blog_latestpostsplugin_tags_fda89e10; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_latestpostsplugin_tags_fda89e10 ON djangocms_blog_latestpostsplugin_tags USING btree (latestpostsplugin_id);


--
-- Name: djangocms_blog_post_36b62cbe; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_36b62cbe ON djangocms_blog_post USING btree (main_image_id);


--
-- Name: djangocms_blog_post_4f331e2f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_4f331e2f ON djangocms_blog_post USING btree (author_id);


--
-- Name: djangocms_blog_post_53808359; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_53808359 ON djangocms_blog_post USING btree (main_image_full_id);


--
-- Name: djangocms_blog_post_9d0a35cc; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_9d0a35cc ON djangocms_blog_post USING btree (main_image_thumbnail_id);


--
-- Name: djangocms_blog_post_categories_efb54956; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_categories_efb54956 ON djangocms_blog_post_categories USING btree (blogcategory_id);


--
-- Name: djangocms_blog_post_categories_f3aa1999; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_categories_f3aa1999 ON djangocms_blog_post_categories USING btree (post_id);


--
-- Name: djangocms_blog_post_e14f02ad; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_e14f02ad ON djangocms_blog_post USING btree (content_id);


--
-- Name: djangocms_blog_post_sites_9365d6e7; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_sites_9365d6e7 ON djangocms_blog_post_sites USING btree (site_id);


--
-- Name: djangocms_blog_post_sites_f3aa1999; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_sites_f3aa1999 ON djangocms_blog_post_sites USING btree (post_id);


--
-- Name: djangocms_blog_post_translat_language_code_9de399a84ef5de4_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_translat_language_code_9de399a84ef5de4_like ON djangocms_blog_post_translation USING btree (language_code varchar_pattern_ops);


--
-- Name: djangocms_blog_post_translation_2dbcba41; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_translation_2dbcba41 ON djangocms_blog_post_translation USING btree (slug);


--
-- Name: djangocms_blog_post_translation_60716c2f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_translation_60716c2f ON djangocms_blog_post_translation USING btree (language_code);


--
-- Name: djangocms_blog_post_translation_90349b61; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_translation_90349b61 ON djangocms_blog_post_translation USING btree (master_id);


--
-- Name: djangocms_blog_post_translation_slug_4f3dfdbb2203287f_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_blog_post_translation_slug_4f3dfdbb2203287f_like ON djangocms_blog_post_translation USING btree (slug varchar_pattern_ops);


--
-- Name: djangocms_inherit_inheritpageplaceholder_ccbb37bf; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_inherit_inheritpageplaceholder_ccbb37bf ON djangocms_inherit_inheritpageplaceholder USING btree (from_page_id);


--
-- Name: djangocms_link_link_d916d256; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_link_link_d916d256 ON djangocms_link_link USING btree (page_link_id);


--
-- Name: djangocms_snippet_snippet_name_259f5ab907cd2d68_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_snippet_snippet_name_259f5ab907cd2d68_like ON djangocms_snippet_snippet USING btree (name varchar_pattern_ops);


--
-- Name: djangocms_snippet_snippetptr_cfd011c9; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_snippet_snippetptr_cfd011c9 ON djangocms_snippet_snippetptr USING btree (snippet_id);


--
-- Name: djangocms_teaser_teaser_d916d256; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX djangocms_teaser_teaser_d916d256 ON djangocms_teaser_teaser USING btree (page_link_id);


--
-- Name: easy_thumbnails_source_b068931c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_source_b068931c ON easy_thumbnails_source USING btree (name);


--
-- Name: easy_thumbnails_source_b454e115; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_source_b454e115 ON easy_thumbnails_source USING btree (storage_hash);


--
-- Name: easy_thumbnails_source_name_53e0b4aeb3d0e1c_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_source_name_53e0b4aeb3d0e1c_like ON easy_thumbnails_source USING btree (name varchar_pattern_ops);


--
-- Name: easy_thumbnails_source_storage_hash_343faac2ddf05af7_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_source_storage_hash_343faac2ddf05af7_like ON easy_thumbnails_source USING btree (storage_hash varchar_pattern_ops);


--
-- Name: easy_thumbnails_thumbnail_0afd9202; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_thumbnail_0afd9202 ON easy_thumbnails_thumbnail USING btree (source_id);


--
-- Name: easy_thumbnails_thumbnail_b068931c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_thumbnail_b068931c ON easy_thumbnails_thumbnail USING btree (name);


--
-- Name: easy_thumbnails_thumbnail_b454e115; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_thumbnail_b454e115 ON easy_thumbnails_thumbnail USING btree (storage_hash);


--
-- Name: easy_thumbnails_thumbnail_name_19b872e1e26d7161_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_thumbnail_name_19b872e1e26d7161_like ON easy_thumbnails_thumbnail USING btree (name varchar_pattern_ops);


--
-- Name: easy_thumbnails_thumbnail_storage_hash_5fd7e681638a428c_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX easy_thumbnails_thumbnail_storage_hash_5fd7e681638a428c_like ON easy_thumbnails_thumbnail USING btree (storage_hash varchar_pattern_ops);


--
-- Name: filer_clipboard_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_clipboard_e8701ad4 ON filer_clipboard USING btree (user_id);


--
-- Name: filer_clipboarditem_2655b062; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_clipboarditem_2655b062 ON filer_clipboarditem USING btree (clipboard_id);


--
-- Name: filer_clipboarditem_814552b9; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_clipboarditem_814552b9 ON filer_clipboarditem USING btree (file_id);


--
-- Name: filer_file_5e7b1936; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_file_5e7b1936 ON filer_file USING btree (owner_id);


--
-- Name: filer_file_a8a44dbb; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_file_a8a44dbb ON filer_file USING btree (folder_id);


--
-- Name: filer_file_d3e32c49; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_file_d3e32c49 ON filer_file USING btree (polymorphic_ctype_id);


--
-- Name: filer_folder_3cfbd988; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folder_3cfbd988 ON filer_folder USING btree (rght);


--
-- Name: filer_folder_5e7b1936; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folder_5e7b1936 ON filer_folder USING btree (owner_id);


--
-- Name: filer_folder_656442a0; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folder_656442a0 ON filer_folder USING btree (tree_id);


--
-- Name: filer_folder_6be37982; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folder_6be37982 ON filer_folder USING btree (parent_id);


--
-- Name: filer_folder_c9e9a848; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folder_c9e9a848 ON filer_folder USING btree (level);


--
-- Name: filer_folder_caf7cc51; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folder_caf7cc51 ON filer_folder USING btree (lft);


--
-- Name: filer_folderpermission_0e939a4f; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folderpermission_0e939a4f ON filer_folderpermission USING btree (group_id);


--
-- Name: filer_folderpermission_a8a44dbb; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folderpermission_a8a44dbb ON filer_folderpermission USING btree (folder_id);


--
-- Name: filer_folderpermission_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX filer_folderpermission_e8701ad4 ON filer_folderpermission USING btree (user_id);


--
-- Name: railshosting_railsbetauser_email_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX railshosting_railsbetauser_email_like ON railshosting_railsbetauser USING btree (email varchar_pattern_ops);


--
-- Name: reversion_revision_b16b0f06; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_revision_b16b0f06 ON reversion_revision USING btree (manager_slug);


--
-- Name: reversion_revision_c69e55a4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_revision_c69e55a4 ON reversion_revision USING btree (date_created);


--
-- Name: reversion_revision_e8701ad4; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_revision_e8701ad4 ON reversion_revision USING btree (user_id);


--
-- Name: reversion_revision_manager_slug_6a1331a19ba6e45_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_revision_manager_slug_6a1331a19ba6e45_like ON reversion_revision USING btree (manager_slug varchar_pattern_ops);


--
-- Name: reversion_version_0c9ba3a3; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_version_0c9ba3a3 ON reversion_version USING btree (object_id_int);


--
-- Name: reversion_version_417f1b1c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_version_417f1b1c ON reversion_version USING btree (content_type_id);


--
-- Name: reversion_version_5de09a8d; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX reversion_version_5de09a8d ON reversion_version USING btree (revision_id);


--
-- Name: taggit_tag_name_47eb69d4457c70fc_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX taggit_tag_name_47eb69d4457c70fc_like ON taggit_tag USING btree (name varchar_pattern_ops);


--
-- Name: taggit_tag_slug_12a2b4e50b24dad3_like; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX taggit_tag_slug_12a2b4e50b24dad3_like ON taggit_tag USING btree (slug varchar_pattern_ops);


--
-- Name: taggit_taggeditem_417f1b1c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX taggit_taggeditem_417f1b1c ON taggit_taggeditem USING btree (content_type_id);


--
-- Name: taggit_taggeditem_76f094bc; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX taggit_taggeditem_76f094bc ON taggit_taggeditem USING btree (tag_id);


--
-- Name: taggit_taggeditem_af31437c; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX taggit_taggeditem_af31437c ON taggit_taggeditem USING btree (object_id);


--
-- Name: ungleich_ungleichpage_f33175e6; Type: INDEX; Schema: public; Owner: app; Tablespace: 
--

CREATE INDEX ungleich_ungleichpage_f33175e6 ON ungleich_ungleichpage USING btree (image_id);


--
-- Name: D1e0ce2e19a5dde4bf91bd55da0f998e; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_categories
    ADD CONSTRAINT "D1e0ce2e19a5dde4bf91bd55da0f998e" FOREIGN KEY (blogcategory_id) REFERENCES djangocms_blog_blogcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D30efff85dc2b8aeb5b0cd15021c7816; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY ungleich_ungleichpage
    ADD CONSTRAINT "D30efff85dc2b8aeb5b0cd15021c7816" FOREIGN KEY (public_extension_id) REFERENCES ungleich_ungleichpage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D3865a3fccba0fef3af61c547c859439; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_globalpagepermission_sites
    ADD CONSTRAINT "D3865a3fccba0fef3af61c547c859439" FOREIGN KEY (globalpagepermission_id) REFERENCES cms_globalpagepermission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D39e972de69b55cc4c8b58e9ca894b94; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_tags
    ADD CONSTRAINT "D39e972de69b55cc4c8b58e9ca894b94" FOREIGN KEY (latestpostsplugin_id) REFERENCES djangocms_blog_latestpostsplugin(cmsplugin_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D98d36523ef8f5a0b35cbf698bd431ed; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_file
    ADD CONSTRAINT "D98d36523ef8f5a0b35cbf698bd431ed" FOREIGN KEY (polymorphic_ctype_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: D9e31d3fcffd61cc4de6d04859c4df85; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_categories
    ADD CONSTRAINT "D9e31d3fcffd61cc4de6d04859c4df85" FOREIGN KEY (blogcategory_id) REFERENCES djangocms_blog_blogcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_content_type_id_7274a4b9a6a80677_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_content_type_id_7274a4b9a6a80677_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group__permission_id_119d0d61842f902_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group__permission_id_119d0d61842f902_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissio_group_id_36c2439f2e68e691_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_group_id_36c2439f2e68e691_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user__permission_id_4ae8a83b6fe9667a_fk_auth_permission_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user__permission_id_4ae8a83b6fe9667a_fk_auth_permission_id FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_56c19fd2fb34f8b9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_56c19fd2fb34f8b9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_user_id_4b4cf591fb57fa1f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_4b4cf591fb57fa1f_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permiss_user_id_4a772bdea6ed34b3_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permiss_user_id_4a772bdea6ed34b3_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: b1a2c98e70ae6118f00567a081b0cb4b; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin_authors
    ADD CONSTRAINT b1a2c98e70ae6118f00567a081b0cb4b FOREIGN KEY (authorentriesplugin_id) REFERENCES djangocms_blog_authorentriesplugin(cmsplugin_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: c25adf4d6104ba67ff886dc9f2a45caf; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post
    ADD CONSTRAINT c25adf4d6104ba67ff886dc9f2a45caf FOREIGN KEY (main_image_thumbnail_id) REFERENCES cmsplugin_filer_image_thumbnailoption(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: c6d96324be133449397f73a9089b4e88; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_image_filerimage
    ADD CONSTRAINT c6d96324be133449397f73a9089b4e88 FOREIGN KEY (thumbnail_option_id) REFERENCES cmsplugin_filer_image_thumbnailoption(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_alias_cmsplugin_ptr_id_5b66c0754b77425f_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_aliaspluginmodel
    ADD CONSTRAINT cms_alias_cmsplugin_ptr_id_5b66c0754b77425f_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_alias_placeholder_id_4d9a049044fc5c62_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_aliaspluginmodel
    ADD CONSTRAINT cms_alias_placeholder_id_4d9a049044fc5c62_fk_cms_placeholder_id FOREIGN KEY (alias_placeholder_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_aliaspluginm_plugin_id_2d8a0ab45136b02f_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_aliaspluginmodel
    ADD CONSTRAINT cms_aliaspluginm_plugin_id_2d8a0ab45136b02f_fk_cms_cmsplugin_id FOREIGN KEY (plugin_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_cmspl_placeholder_id_2e3fbdcc67d364ed_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmspl_placeholder_id_2e3fbdcc67d364ed_fk_cms_placeholder_id FOREIGN KEY (placeholder_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_cmsplugin_parent_id_5d27fb648727d04c_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_cmsplugin
    ADD CONSTRAINT cms_cmsplugin_parent_id_5d27fb648727d04c_fk_cms_cmsplugin_id FOREIGN KEY (parent_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_globalpagepermis_group_id_7cda09038f64b58f_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_globalpagepermission
    ADD CONSTRAINT cms_globalpagepermis_group_id_7cda09038f64b58f_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_globalpagepermis_site_id_214c6cfe2b65c86d_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_globalpagepermission_sites
    ADD CONSTRAINT cms_globalpagepermis_site_id_214c6cfe2b65c86d_fk_django_site_id FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_globalpagepermissi_user_id_2380d7172364bbc9_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_globalpagepermission
    ADD CONSTRAINT cms_globalpagepermissi_user_id_2380d7172364bbc9_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_p_placeholder_ref_id_22fdc868550a613b_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_placeholderreference
    ADD CONSTRAINT cms_p_placeholder_ref_id_22fdc868550a613b_fk_cms_placeholder_id FOREIGN KEY (placeholder_ref_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page_p_placeholder_id_3e31dd5cf07a7a3_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page_placeholders
    ADD CONSTRAINT cms_page_p_placeholder_id_3e31dd5cf07a7a3_fk_cms_placeholder_id FOREIGN KEY (placeholder_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page_parent_id_8d51c5e4e7e9310_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_parent_id_8d51c5e4e7e9310_fk_cms_page_id FOREIGN KEY (parent_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page_placeholders_page_id_26147522c2da834f_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page_placeholders
    ADD CONSTRAINT cms_page_placeholders_page_id_26147522c2da834f_fk_cms_page_id FOREIGN KEY (page_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page_publisher_public_id_70c1b7f7287e96c2_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_publisher_public_id_70c1b7f7287e96c2_fk_cms_page_id FOREIGN KEY (publisher_public_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_page_site_id_25555bc4ab6e5908_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_page
    ADD CONSTRAINT cms_page_site_id_25555bc4ab6e5908_fk_django_site_id FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pagepermission_group_id_214b54c538a2060b_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pagepermission
    ADD CONSTRAINT cms_pagepermission_group_id_214b54c538a2060b_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pagepermission_page_id_742205a7841c852d_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pagepermission
    ADD CONSTRAINT cms_pagepermission_page_id_742205a7841c852d_fk_cms_page_id FOREIGN KEY (page_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pagepermission_user_id_1fd8f6bd6e393a1d_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pagepermission
    ADD CONSTRAINT cms_pagepermission_user_id_1fd8f6bd6e393a1d_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pageuser_created_by_id_4db03915f07f3a7b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pageuser
    ADD CONSTRAINT cms_pageuser_created_by_id_4db03915f07f3a7b_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pageuser_user_ptr_id_4eddb8b96660e195_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pageuser
    ADD CONSTRAINT cms_pageuser_user_ptr_id_4eddb8b96660e195_fk_auth_user_id FOREIGN KEY (user_ptr_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pageusergrou_group_ptr_id_5b59774f60d55d66_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pageusergroup
    ADD CONSTRAINT cms_pageusergrou_group_ptr_id_5b59774f60d55d66_fk_auth_group_id FOREIGN KEY (group_ptr_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_pageusergroup_created_by_id_9472032c154ad4d_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_pageusergroup
    ADD CONSTRAINT cms_pageusergroup_created_by_id_9472032c154ad4d_fk_auth_user_id FOREIGN KEY (created_by_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_place_cmsplugin_ptr_id_7bde01ee40fae1cc_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_placeholderreference
    ADD CONSTRAINT cms_place_cmsplugin_ptr_id_7bde01ee40fae1cc_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_staticplac_public_id_638640ab8c6be6d4_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplac_public_id_638640ab8c6be6d4_fk_cms_placeholder_id FOREIGN KEY (public_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_staticplace_draft_id_5976d579de303795_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplace_draft_id_5976d579de303795_fk_cms_placeholder_id FOREIGN KEY (draft_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_staticplaceholder_site_id_c16ce69f477cc55_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_staticplaceholder
    ADD CONSTRAINT cms_staticplaceholder_site_id_c16ce69f477cc55_fk_django_site_id FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_title_page_id_672fdd0b4938090d_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_page_id_672fdd0b4938090d_fk_cms_page_id FOREIGN KEY (page_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_title_publisher_public_id_63837c0040e816c0_fk_cms_title_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_title
    ADD CONSTRAINT cms_title_publisher_public_id_63837c0040e816c0_fk_cms_title_id FOREIGN KEY (publisher_public_id) REFERENCES cms_title(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_userset_clipboard_id_40153078a366ee92_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_usersettings
    ADD CONSTRAINT cms_userset_clipboard_id_40153078a366ee92_fk_cms_placeholder_id FOREIGN KEY (clipboard_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cms_usersettings_user_id_422e300cea4d3119_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cms_usersettings
    ADD CONSTRAINT cms_usersettings_user_id_422e300cea4d3119_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin__cmsplugin_ptr_id_d866216c862b96c_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_teaser_filerteaser
    ADD CONSTRAINT cmsplugin__cmsplugin_ptr_id_d866216c862b96c_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin__image_id_28232731ed1ae7db_fk_filer_image_file_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_teaser_filerteaser
    ADD CONSTRAINT cmsplugin__image_id_28232731ed1ae7db_fk_filer_image_file_ptr_id FOREIGN KEY (image_id) REFERENCES filer_image(file_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_cmsplugin_ptr_id_2906a73bda08a0df_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_file_filerfile
    ADD CONSTRAINT cmsplugin_cmsplugin_ptr_id_2906a73bda08a0df_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_cmsplugin_ptr_id_4adeb50a9dc2e688_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_folder_filerfolder
    ADD CONSTRAINT cmsplugin_cmsplugin_ptr_id_4adeb50a9dc2e688_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_cmsplugin_ptr_id_548d56148a213c9d_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_video_filervideo
    ADD CONSTRAINT cmsplugin_cmsplugin_ptr_id_548d56148a213c9d_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_cmsplugin_ptr_id_5b8b7a1fef686524_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_link_filerlinkplugin
    ADD CONSTRAINT cmsplugin_cmsplugin_ptr_id_5b8b7a1fef686524_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_cmsplugin_ptr_id_7f712f0346ee6a25_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_image_filerimage
    ADD CONSTRAINT cmsplugin_cmsplugin_ptr_id_7f712f0346ee6a25_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_f_image_id_387c5358f32cb24_fk_filer_image_file_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_video_filervideo
    ADD CONSTRAINT cmsplugin_f_image_id_387c5358f32cb24_fk_filer_image_file_ptr_id FOREIGN KEY (image_id) REFERENCES filer_image(file_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_f_image_id_7185b59bafa7f6c_fk_filer_image_file_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_image_filerimage
    ADD CONSTRAINT cmsplugin_f_image_id_7185b59bafa7f6c_fk_filer_image_file_ptr_id FOREIGN KEY (image_id) REFERENCES filer_image(file_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer__file_link_id_5b4906e85dc229c5_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_image_filerimage
    ADD CONSTRAINT cmsplugin_filer__file_link_id_5b4906e85dc229c5_fk_filer_file_id FOREIGN KEY (file_link_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_f_folder_id_50feb55a240d8315_fk_filer_folder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_folder_filerfolder
    ADD CONSTRAINT cmsplugin_filer_f_folder_id_50feb55a240d8315_fk_filer_folder_id FOREIGN KEY (folder_id) REFERENCES filer_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_file__file_id_4007a229f0c0340f_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_file_filerfile
    ADD CONSTRAINT cmsplugin_filer_file__file_id_4007a229f0c0340f_fk_filer_file_id FOREIGN KEY (file_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_im_page_link_id_7d07a44d6b75a570_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_image_filerimage
    ADD CONSTRAINT cmsplugin_filer_im_page_link_id_7d07a44d6b75a570_fk_cms_page_id FOREIGN KEY (page_link_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_li_page_link_id_1d3c572fcb96fa9f_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_link_filerlinkplugin
    ADD CONSTRAINT cmsplugin_filer_li_page_link_id_1d3c572fcb96fa9f_fk_cms_page_id FOREIGN KEY (page_link_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_link__file_id_45178508a0703e54_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_link_filerlinkplugin
    ADD CONSTRAINT cmsplugin_filer_link__file_id_45178508a0703e54_fk_filer_file_id FOREIGN KEY (file_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_te_page_link_id_6c65f47473426d49_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_teaser_filerteaser
    ADD CONSTRAINT cmsplugin_filer_te_page_link_id_6c65f47473426d49_fk_cms_page_id FOREIGN KEY (page_link_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: cmsplugin_filer_vide_movie_id_169f89b271c3cbff_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY cmsplugin_filer_video_filervideo
    ADD CONSTRAINT cmsplugin_filer_vide_movie_id_169f89b271c3cbff_fk_filer_file_id FOREIGN KEY (movie_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: de79cf81884893c0358d274266cd1d97; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post
    ADD CONSTRAINT de79cf81884893c0358d274266cd1d97 FOREIGN KEY (main_image_full_id) REFERENCES cmsplugin_filer_image_thumbnailoption(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dj_parent_id_124c3ea43cd571bb_fk_djangocms_blog_blogcategory_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_blogcategory
    ADD CONSTRAINT dj_parent_id_124c3ea43cd571bb_fk_djangocms_blog_blogcategory_id FOREIGN KEY (parent_id) REFERENCES djangocms_blog_blogcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dja_master_id_1e34ae93e58bb4c_fk_djangocms_blog_blogcategory_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_blogcategory_translation
    ADD CONSTRAINT dja_master_id_1e34ae93e58bb4c_fk_djangocms_blog_blogcategory_id FOREIGN KEY (master_id) REFERENCES djangocms_blog_blogcategory(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: dja_snippet_id_199da8772ac20aab_fk_djangocms_snippet_snippet_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_snippet_snippetptr
    ADD CONSTRAINT dja_snippet_id_199da8772ac20aab_fk_djangocms_snippet_snippet_id FOREIGN KEY (snippet_id) REFERENCES djangocms_snippet_snippet(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djan_content_type_id_3487bc4d3dd77d88_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT djan_content_type_id_3487bc4d3dd77d88_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djang_main_image_id_7be928a6d76ca21e_fk_filer_image_file_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post
    ADD CONSTRAINT djang_main_image_id_7be928a6d76ca21e_fk_filer_image_file_ptr_id FOREIGN KEY (main_image_id) REFERENCES filer_image(file_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_51952f5a1f098171_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_51952f5a1f098171_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms__master_id_6f2734d5156341c8_fk_djangocms_blog_post_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_translation
    ADD CONSTRAINT djangocms__master_id_6f2734d5156341c8_fk_djangocms_blog_post_id FOREIGN KEY (master_id) REFERENCES djangocms_blog_post(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_bl_post_id_554ac9016e77fd4a_fk_djangocms_blog_post_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_sites
    ADD CONSTRAINT djangocms_bl_post_id_554ac9016e77fd4a_fk_djangocms_blog_post_id FOREIGN KEY (post_id) REFERENCES djangocms_blog_post(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_bl_post_id_72c09b2d1fa023e8_fk_djangocms_blog_post_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_categories
    ADD CONSTRAINT djangocms_bl_post_id_72c09b2d1fa023e8_fk_djangocms_blog_post_id FOREIGN KEY (post_id) REFERENCES djangocms_blog_post(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_blo_content_id_7c060747899bb391_fk_cms_placeholder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post
    ADD CONSTRAINT djangocms_blo_content_id_7c060747899bb391_fk_cms_placeholder_id FOREIGN KEY (content_id) REFERENCES cms_placeholder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_blog_authore_user_id_7c4f4da038a9db62_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin_authors
    ADD CONSTRAINT djangocms_blog_authore_user_id_7c4f4da038a9db62_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_blog_latestp_tag_id_66d8da2f4531c2b9_fk_taggit_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_tags
    ADD CONSTRAINT djangocms_blog_latestp_tag_id_66d8da2f4531c2b9_fk_taggit_tag_id FOREIGN KEY (tag_id) REFERENCES taggit_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_blog_post_author_id_740f4c9aed461f1f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post
    ADD CONSTRAINT djangocms_blog_post_author_id_740f4c9aed461f1f_fk_auth_user_id FOREIGN KEY (author_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_blog_post_s_site_id_173d1131dbce5a3_fk_django_site_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_post_sites
    ADD CONSTRAINT djangocms_blog_post_s_site_id_173d1131dbce5a3_fk_django_site_id FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_42bfc10438d134b2_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_teaser_teaser
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_42bfc10438d134b2_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_50f54fddfff30903_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_authorentriesplugin
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_50f54fddfff30903_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_52c42fffa4fb4c95_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_googlemap_googlemap
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_52c42fffa4fb4c95_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_5edeb98aae85a226_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_5edeb98aae85a226_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_64d16f645cff9ca5_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_inherit_inheritpageplaceholder
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_64d16f645cff9ca5_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_68e16566c8a3af59_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_link_link
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_68e16566c8a3af59_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_7617c6dca52b79d1_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_snippet_snippetptr
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_7617c6dca52b79d1_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_cmsplugin_ptr_id_795f32e5dde2b503_fk_cms_cmsplugin_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_flash_flash
    ADD CONSTRAINT djangocms_cmsplugin_ptr_id_795f32e5dde2b503_fk_cms_cmsplugin_id FOREIGN KEY (cmsplugin_ptr_id) REFERENCES cms_cmsplugin(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_inherit__from_page_id_1df18740f2d56346_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_inherit_inheritpageplaceholder
    ADD CONSTRAINT djangocms_inherit__from_page_id_1df18740f2d56346_fk_cms_page_id FOREIGN KEY (from_page_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_link_lin_page_link_id_1331b5c52df0936a_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_link_link
    ADD CONSTRAINT djangocms_link_lin_page_link_id_1331b5c52df0936a_fk_cms_page_id FOREIGN KEY (page_link_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: djangocms_teaser_t_page_link_id_27e63cbd6347058f_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_teaser_teaser
    ADD CONSTRAINT djangocms_teaser_t_page_link_id_27e63cbd6347058f_fk_cms_page_id FOREIGN KEY (page_link_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: e_thumbnail_id_43080364cf301698_fk_easy_thumbnails_thumbnail_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY easy_thumbnails_thumbnaildimensions
    ADD CONSTRAINT e_thumbnail_id_43080364cf301698_fk_easy_thumbnails_thumbnail_id FOREIGN KEY (thumbnail_id) REFERENCES easy_thumbnails_thumbnail(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: easy_th_source_id_6f8372984cc2bf35_fk_easy_thumbnails_source_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY easy_thumbnails_thumbnail
    ADD CONSTRAINT easy_th_source_id_6f8372984cc2bf35_fk_easy_thumbnails_source_id FOREIGN KEY (source_id) REFERENCES easy_thumbnails_source(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: fbc5046808bf20fc0670675b9967abfb; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY djangocms_blog_latestpostsplugin_categories
    ADD CONSTRAINT fbc5046808bf20fc0670675b9967abfb FOREIGN KEY (latestpostsplugin_id) REFERENCES djangocms_blog_latestpostsplugin(cmsplugin_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_clipb_clipboard_id_5b26c240ff889721_fk_filer_clipboard_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_clipboarditem
    ADD CONSTRAINT filer_clipb_clipboard_id_5b26c240ff889721_fk_filer_clipboard_id FOREIGN KEY (clipboard_id) REFERENCES filer_clipboard(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_clipboard_user_id_3674b01d0559f7d_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_clipboard
    ADD CONSTRAINT filer_clipboard_user_id_3674b01d0559f7d_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_clipboarditem_file_id_5b0f53b76815c091_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_clipboarditem
    ADD CONSTRAINT filer_clipboarditem_file_id_5b0f53b76815c091_fk_filer_file_id FOREIGN KEY (file_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_file_folder_id_e318a07985894d4_fk_filer_folder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_file
    ADD CONSTRAINT filer_file_folder_id_e318a07985894d4_fk_filer_folder_id FOREIGN KEY (folder_id) REFERENCES filer_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_file_owner_id_5bff3f10c7d5b16a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_file
    ADD CONSTRAINT filer_file_owner_id_5bff3f10c7d5b16a_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folder_owner_id_76418f490e43e78a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folder
    ADD CONSTRAINT filer_folder_owner_id_76418f490e43e78a_fk_auth_user_id FOREIGN KEY (owner_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folder_parent_id_32445c3f610191b9_fk_filer_folder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folder
    ADD CONSTRAINT filer_folder_parent_id_32445c3f610191b9_fk_filer_folder_id FOREIGN KEY (parent_id) REFERENCES filer_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folderpermis_folder_id_73f63d5b9223dc8_fk_filer_folder_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folderpermission
    ADD CONSTRAINT filer_folderpermis_folder_id_73f63d5b9223dc8_fk_filer_folder_id FOREIGN KEY (folder_id) REFERENCES filer_folder(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folderpermissio_group_id_68fed69352f6930_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folderpermission
    ADD CONSTRAINT filer_folderpermissio_group_id_68fed69352f6930_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_folderpermission_user_id_4e0c62cfd3e30c58_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_folderpermission
    ADD CONSTRAINT filer_folderpermission_user_id_4e0c62cfd3e30c58_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: filer_image_file_ptr_id_2e1e3365e09fa79f_fk_filer_file_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY filer_image
    ADD CONSTRAINT filer_image_file_ptr_id_2e1e3365e09fa79f_fk_filer_file_id FOREIGN KEY (file_ptr_id) REFERENCES filer_file(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reve_content_type_id_16723ee6ef091b59_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY reversion_version
    ADD CONSTRAINT reve_content_type_id_16723ee6ef091b59_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reversion_revision_id_220bd32d7f58c93b_fk_reversion_revision_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY reversion_version
    ADD CONSTRAINT reversion_revision_id_220bd32d7f58c93b_fk_reversion_revision_id FOREIGN KEY (revision_id) REFERENCES reversion_revision(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reversion_revision_user_id_4a94651b12ab7cbf_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY reversion_revision
    ADD CONSTRAINT reversion_revision_user_id_4a94651b12ab7cbf_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tagg_content_type_id_273e2c3f8a3e6d0d_fk_django_content_type_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT tagg_content_type_id_273e2c3f8a3e6d0d_fk_django_content_type_id FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: taggit_taggeditem_tag_id_3e9eb5e3a6fbca77_fk_taggit_tag_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY taggit_taggeditem
    ADD CONSTRAINT taggit_taggeditem_tag_id_3e9eb5e3a6fbca77_fk_taggit_tag_id FOREIGN KEY (tag_id) REFERENCES taggit_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ungleich_u_image_id_5cd0910b381bed14_fk_filer_image_file_ptr_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY ungleich_ungleichpage
    ADD CONSTRAINT ungleich_u_image_id_5cd0910b381bed14_fk_filer_image_file_ptr_id FOREIGN KEY (image_id) REFERENCES filer_image(file_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: ungleich_ung_extended_object_id_683caa456269379e_fk_cms_page_id; Type: FK CONSTRAINT; Schema: public; Owner: app
--

ALTER TABLE ONLY ungleich_ungleichpage
    ADD CONSTRAINT ungleich_ung_extended_object_id_683caa456269379e_fk_cms_page_id FOREIGN KEY (extended_object_id) REFERENCES cms_page(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\connect postgres

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

\connect template1

SET default_transaction_read_only = off;

--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: template1; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE template1 IS 'default template for new databases';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

--
-- PostgreSQL database cluster dump complete
--

