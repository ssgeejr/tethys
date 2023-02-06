SET @rid = 0;

select 
	riskid as rid,
	count(distinct hash) as total
from
	scorecard
where
	dtkey = '0422A'
    and riskid = @rid
    and hash not in (
		select
			distinct hash
		from 
			scorecard
		where
			dtkey = '0322B'
            and riskid = @rid
	)
group by
	rid;