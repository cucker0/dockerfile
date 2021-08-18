# Web Stress Testing



## What is webstress

A Web Stress Testing tool.

## Supported tags and respective `Dockerfile` links
* [`1.0`, `1`,  `1.0-centos:8`](https://github.com/cucker0/dockerfile/blob/main/web_stress_testing/df/Dockerfile)

## Component
* ab (apache)
* siege

## How to use this image

### run image
```
docker run --rm -it cucker/webstress:1
```

### ab
support http/https

* Usage
    ```
    Usage: ab [options] [http[s]://]hostname[:port]/path
    Options are:
        -n requests     Number of requests to perform
        -c concurrency  Number of multiple requests to make at a time
        -t timelimit    Seconds to max. to spend on benchmarking
                        This implies -n 50000
        -s timeout      Seconds to max. wait for each response
                        Default is 30 seconds
        -b windowsize   Size of TCP send/receive buffer, in bytes
        -B address      Address to bind to when making outgoing connections
        -p postfile     File containing data to POST. Remember also to set -T
        -u putfile      File containing data to PUT. Remember also to set -T
        -T content-type Content-type header to use for POST/PUT data, eg.
                        'application/x-www-form-urlencoded'
                        Default is 'text/plain'
        -v verbosity    How much troubleshooting info to print
        -w              Print out results in HTML tables
        -i              Use HEAD instead of GET
        -x attributes   String to insert as table attributes
        -y attributes   String to insert as tr attributes
        -z attributes   String to insert as td or th attributes
        -C attribute    Add cookie, eg. 'Apache=1234'. (repeatable)
        -H attribute    Add Arbitrary header line, eg. 'Accept-Encoding: gzip'
                        Inserted after all normal header lines. (repeatable)
        -A attribute    Add Basic WWW Authentication, the attributes
                        are a colon separated username and password.
        -P attribute    Add Basic Proxy Authentication, the attributes
                        are a colon separated username and password.
        -X proxy:port   Proxyserver and port number to use
        -V              Print version number and exit
        -k              Use HTTP KeepAlive feature
        -d              Do not show percentiles served table.
        -S              Do not show confidence estimators and warnings.
        -q              Do not show progress when doing more than 150 requests
        -l              Accept variable document length (use this for dynamic pages)
        -g filename     Output collected data to gnuplot format file.
        -e filename     Output CSV file with percentages served
        -r              Don't exit on socket receive errors.
        -m method       Method name
        -h              Display usage information (this message)
        -I              Disable TLS Server Name Indication (SNI) extension
        -Z ciphersuite  Specify SSL/TLS cipher suite (See openssl ciphers)
        -f protocol     Specify SSL/TLS protocol
                        (SSL2, TLS1, TLS1.1, TLS1.2 or ALL)
        -E certfile     Specify optional client certificate chain and private key
    ```

* Example
    ```
    ab -c 1000 -n 5000 https://www.baidu.com/
    ```

### siege
support http/https

* Usage
    ```
    SIEGE 4.1.1
    Usage: siege [options]
           siege [options] URL
           siege -g URL
    Options:
      -V, --version             VERSION, prints the version number.
      -h, --help                HELP, prints this section.
      -C, --config              CONFIGURATION, show the current config.
      -v, --verbose             VERBOSE, prints notification to screen.
      -q, --quiet               QUIET turns verbose off and suppresses output.
      -g, --get                 GET, pull down HTTP headers and display the
                                transaction. Great for application debugging.
      -p, --print               PRINT, like GET only it prints the entire page.
      -c, --concurrent=NUM      CONCURRENT users, default is 10
      -r, --reps=NUM            REPS, number of times to run the test.
      -t, --time=NUMm           TIMED testing where "m" is modifier S, M, or H
                                ex: --time=1H, one hour test.
      -d, --delay=NUM           Time DELAY, random delay before each request
      -b, --benchmark           BENCHMARK: no delays between requests.
      -i, --internet            INTERNET user simulation, hits URLs randomly.
      -f, --file=FILE           FILE, select a specific URLS FILE.
      -R, --rc=FILE             RC, specify an siegerc file
      -l, --log[=FILE]          LOG to FILE. If FILE is not specified, the
                                default is used: PREFIX/var/siege.log
      -m, --mark="text"         MARK, mark the log file with a string.
                                between .001 and NUM. (NOT COUNTED IN STATS)
      -H, --header="text"       Add a header to request (can be many)
      -A, --user-agent="text"   Sets User-Agent in request
      -T, --content-type="text" Sets Content-Type in request
      -j, --json-output         JSON OUTPUT, print final stats to stdout as JSON
          --no-parser           NO PARSER, turn off the HTML page parser
          --no-follow           NO FOLLOW, do not follow HTTP redirects
    ```


* Example
    ```
    siege -c 100 -r 10 url
    siege -c 200 -t 6S url
    ```

#### bombardment
* Usage
    ```
    bombardment [urlfile] [inital # of clients] [inc value] [# of inc] [delay]
    ```