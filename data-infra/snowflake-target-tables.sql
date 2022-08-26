USE ROLE DBT_TEMPLATE_PROJECT_TRANSFORMER;

CREATE SCHEMA DBT_TEMPLATE_PROJECT_DATABASE.WEBSITE;
CREATE SCHEMA DBT_TEMPLATE_PROJECT_DATABASE.workday;
CREATE SCHEMA DBT_TEMPLATE_PROJECT_DATABASE.analytics;

CREATE OR REPLACE TABLE DBT_TEMPLATE_PROJECT_DATABASE.WORKDAY.DATA_EMPLOYEES (
    "First Name" string,
    "Last Name" string,
    "Birth Date" string,
    "Email" string,
    "Hobby" string,
    "Experience" bigint,
    "Start Date" timestamp,
    "Salary" bigint,
    "City" string,
    "Nationality" string,
    "Skill" string,
    effective_from_ts timestamp
)
;
CREATE OR REPLACE TABLE DBT_TEMPLATE_PROJECT_DATABASE.WEBSITE.web_events (
    "Event ID" string,
    "Email" string,
    "Event Start" timestamp,
    "Event End" timestamp,
    "Web Event Type" string,
    "Content ID" string,
    effective_from_ts timestamp
)
;

CREATE OR REPLACE TABLE DBT_TEMPLATE_PROJECT_DATABASE.WEBSITE.sub_deactivate (
    "Event ID" string,
     "Email" string,
     "End Date" timestamp,
     "Subscription Termination Reason" string,
     effective_from_ts timestamp
);
CREATE OR REPLACE TABLE DBT_TEMPLATE_PROJECT_DATABASE.WEBSITE.sub_activate (
    "Event ID" string,
     "First Name" string,
     "Last Name" string,
     "Birth Date" string,
     "Email" string,
    "Start Date" timestamp,
     "City" string,
     "Nationality" string,
     "Subscription Type" string,
     effective_from_ts timestamp
    );

CREATE OR REPLACE TABLE DBT_TEMPLATE_PROJECT_DATABASE.WEBSITE.content (
    "Content Name" string,
     "Content ID" string,
     "Genre" string,
     "Sub Genre" string,
     "Instrument" string,
    "Instrument Category" string,
    "Email" string,
    effective_from_ts timestamp
);
