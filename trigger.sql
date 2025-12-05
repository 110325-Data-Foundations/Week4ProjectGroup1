CREATE OR REPLACE FUNCTION public.log_team_insert()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO public.teams_log (team_id, action, details)
    VALUES (
        NEW.team_id,
        'INSERT',
        format('New team "%s" has been created', NEW.team_id)
    );

    RETURN NEW;
END;
$$;


CREATE TRIGGER team_insert_audit_trigger
AFTER INSERT ON public.teams
FOR EACH ROW 
EXECUTE FUNCTION public.log_team_insert();