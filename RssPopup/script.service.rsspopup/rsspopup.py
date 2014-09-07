import feedparser
import xbmc
import xbmcaddon

rsspopup = xbmcaddon.Addon(id='script.service.rsspopup')
icon = rsspopup.getAddonInfo('icon')

published, etag_value, tick = "", "none", 4

while (not xbmc.abortRequested):
	if tick == 0:
		tick = 30 * max(1, int(rsspopup.getSetting('interval')))
		feedurl = rsspopup.getSetting('feedurl')
		if feedurl == "--custom--":
			feedurl = rsspopup.getSetting('customurl')
		xbmc.log("rsspopup: RSS feed URL is "+feedurl, level=xbmc.LOGDEBUG)
		data = feedparser.parse(feedurl, etag=etag_value)
		if int(getattr(data, 'status', 200)) >= 400:
			xbmc.log("rsspopup: RSS feed URL is "+feedurl+" status code is "+str(data.status), level=xbmc.LOGDEBUG)
			xbmc.log("rsspopup: interval is "+str(maxtick), level=xbmc.LOGDEBUG)
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(rsspopup.getLocalizedString(32005), str(data.status)+": "+feedurl, 10000, icon))
			break
		if hasattr(data, 'etag'):
			etag_value = data.etag
		if len(data.entries) > 0:
			lastPub = str(data.entries[0].published)
			if published != lastPub:
				published = lastPub
				if rsspopup.getSetting('showdesc') == "true":
					description = data.entries[0].description.encode("utf-8","ignore");
					showtime = 1000 * max(15, min(25, len(description.split())))
					xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(data.entries[0].title.encode("utf-8","ignore"), description, showtime, icon))
				else:
					text = data.entries[0].title.encode("utf-8","ignore")
					xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(text, text, 10000, icon))
		else:
			xbmc.log("rsspopup: no entries for "+feedurl, level=xbmc.LOGDEBUG)		
 	tick = tick - 1
 	xbmc.sleep(2000)