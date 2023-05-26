# queryperf


## What's queryperf
Queryperf is a DNS server query performance testing tool.
This image build with queryperf v1.12.

## Supported tags and respective `Dockerfile` links
* [`1.0`, `latest`](https://github.com/cucker0/dockerfile/blob/main/queryperf/Dockerfile)

## How does it work
Copy the queryperf binary file from docker to the host `/usr/bin/`, then you can use the queryperf command.

## How to use this image
1. Run a container with cucker/queryperf image.
    ```bash
    docker run --rm -v /usr/bin:/pkg cucker/queryperf
    ```
    It will copy queryperf file from docker to host(/usr/bin/queryperf).

2. Use queryperf command in Host.

## How to use queryperf
* Usage of queryperf 
    ```bash
    $ queryperf -h

    DNS Query Performance Testing Tool
    Version: $Id: queryperf.c,v 1.12 2007/09/05 07:36:04 marka Exp $


    Usage: queryperf [-d datafile] [-s server_addr] [-p port] [-q num_queries]
                     [-b bufsize] [-t timeout] [-n] [-l limit] [-f family] [-1]
                     [-i interval] [-r arraysize] [-u unit] [-H histfile]
                     [-T qps] [-e] [-D] [-R] [-c] [-v] [-h]
      -d specifies the input data file (default: stdin)
      -s sets the server to query (default: 127.0.0.1)
      -p sets the port on which to query the server (default: 53)
      -q specifies the maximum number of queries outstanding (default: 20)
      -t specifies the timeout for query completion in seconds (default: 5)
      -n causes configuration changes to be ignored
      -l specifies how a limit for how long to run tests in seconds (no default)
      -1 run through input only once (default: multiple iff limit given)
      -b set input/output buffer size in kilobytes (default: 32 k)
      -i specifies interval of intermediate outputs in seconds (default: 0=none)
      -f specify address family of DNS transport, inet or inet6 (default: any)
      -r set RTT statistics array size (default: 50000)
      -u set RTT statistics time unit in usec (default: 100)
      -H specifies RTT histogram data file (default: none)
      -T specify the target qps (default: 0=unspecified)
      -e enable EDNS 0
      -D set the DNSSEC OK bit (implies EDNS)
      -R disable recursion
      -c print the number of packets with each rcode
      -v verbose: report the RCODE of each response on stdout
      -h print this usage
    ```

* Example for stress testing
    1. Prepare an RR sample file.
        cat ./1000rr.txt 
        ```bash
        dns.zz.com A
        10.100.240.133 PTR
        zz.com SOA
        10.100.240.133 PTR
        dns.zz.com A
        zz.com SOA
        go.com MX
        go.com MX
        zz.com SOA
        liangxi.go.com CNAME
        ```
    2. exec queryperf
        ```bash
        queryperf -d ./1000rr.txt -s 10.100.240.136 -p 53
        ```

## Project
[queryperf](https://github.com/cucker0/dockerfile/blob/main/queryperf)