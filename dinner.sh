#! /bin/bash
NAMES=( "" "Starters" "" "Main courses" "" "" "" "Deserts")

# New command
curl -s "https://55-amsterdam.sohappy.work/?e=zr&id=1968"
curl -s "https://55-amsterdam.sohappy.work/?e=zro.start&d=16-07-2019&id=1968"
for ID in 1 3 7
do
    echo ${NAMES[$ID]} ":"

		URL="https://55-amsterdam.sohappy.work/?e=zro.cr&crid=$ID&id=1968"
		AGENT="User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0"
		ACCEPT="Accept: */*' -H 'Accept-Language: en-US,en;q=0.5"
		REFERER="Referer: https://55-amsterdam.sohappy.work/index.cfm?e=zr&id=1968"
		WITH="X-Requested-With: XMLHttpRequest"
		DNT='DNT: 1'
		ALIVE='Connection: keep-alive'
		COOKIE='Cookie: CFID=6972889; CFTOKEN=b95b64a25ce32d4-43A81DFB-F404-88EC-0AABA394BCE4721A; ICMD=1; JSESSIONID=8BA9CD57AD728BBDA942A17232FEEC78.instance2'
		TRAILERS='TE: Trailers'

    RESPONSE=`curl -s "$URL" -H "$AGENT" -H "$ACCEPT" --compressed -H "$REFERER" -H "$WITH" -H "$DNT" -H "$ALIVE" -H "$COOKIE" -H "$TRAILERS" --data ''`
    MEALS=`echo $RESPONSE | pup div.product-box text{}`
		echo $MEALS
done
