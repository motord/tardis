-- Function: bot.foxtrot()

-- DROP FUNCTION bot.foxtrot();

CREATE OR REPLACE FUNCTION bot.foxtrot()
  RETURNS json AS
$BODY$import json
return json.dumps({"dance": "foxtrot"})$BODY$
  LANGUAGE plpythonu VOLATILE
  COST 100;
ALTER FUNCTION bot.foxtrot()
  OWNER TO tardis;
