-- Function: bot.waltz()

-- DROP FUNCTION bot.waltz();

CREATE OR REPLACE FUNCTION bot.waltz()
  RETURNS json AS
$BODY$import json
return json.dumps({"dance": "waltz"})$BODY$
  LANGUAGE plpythonu VOLATILE
  COST 100;
ALTER FUNCTION bot.waltz()
  OWNER TO tardis;
