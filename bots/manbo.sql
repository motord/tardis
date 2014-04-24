-- Function: bot.manbo()

-- DROP FUNCTION bot.manbo();

CREATE OR REPLACE FUNCTION bot.manbo()
  RETURNS json AS
$BODY$import json
return json.dumps({"dance": "manbo"})$BODY$
  LANGUAGE plpythonu VOLATILE
  COST 100;
ALTER FUNCTION bot.manbo()
  OWNER TO tardis;
