<html>
<head>
<script>
</script>

</head>	

<body>
    <div>
        <div>id: {{id}}</div>
        <div>name: {{name}}</div>
        <div>status: {{status}}</div>
        <div>last updated: {{last_updated}}</div>
        % if uptime:
            <div>update time: {{uptime}}</div>
        % end
    </div>

    <div>
        <div>Ping status: {{"offline" if ping_response else "online"}}</div>

        % if status == 1:
            <span>
                <a href="/brix2807/suspend">Suspend Brix2807</a>
                <a href="/brix2807/shutdown">Shutdown Brix2807</a>
            </span>
        % else:
            <span><a href="/brix2807/wake">Wake Brix2807</a></span>
        % end

    </div>

</body>

</html>