-- Function: bot.tango()

-- DROP FUNCTION bot.tango();

CREATE OR REPLACE FUNCTION bot.tango()
  RETURNS json AS
$BODY$import json
return json.dumps({"dance": "tango"})$BODY$
  LANGUAGE plpythonu VOLATILE
  COST 100;
ALTER FUNCTION bot.tango()
  OWNER TO tardis;
