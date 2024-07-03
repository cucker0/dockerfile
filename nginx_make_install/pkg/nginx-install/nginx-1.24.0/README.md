# nginx_1.24.0


## 问题
### 问题1

journalctl -xeu nginx.service
```bash
May 17 23:15:54 dns-node3 nginx[91561]: nginx: [alert] detected a LuaJIT version which is not OpenResty's; many optimizations will be disabled and performance will be compromised (>
May 17 23:15:54 dns-node3 nginx[91561]: nginx: [alert] failed to load the 'resty.core' module (https://github.com/openresty/lua-resty-core); ensure you are using an OpenResty relea>
May 17 23:15:54 dns-node3 nginx[91561]:         no field package.preload['resty.core']
May 17 23:15:54 dns-node3 nginx[91561]:         no file './resty/core.lua'
May 17 23:15:54 dns-node3 nginx[91561]:         no file '/usr/local/share/luajit-2.1.0-beta3/resty/core.lua'
May 17 23:15:54 dns-node3 nginx[91561]:         no file '/usr/local/share/lua/5.1/resty/core.lua'
May 17 23:15:54 dns-node3 nginx[91561]:         no file '/usr/local/share/lua/5.1/resty/core/init.lua'
May 17 23:15:54 dns-node3 nginx[91561]:         no file './resty/core.so'
May 17 23:15:54 dns-node3 nginx[91561]:         no file '/usr/local/lib/lua/5.1/resty/core.so'
May 17 23:15:54 dns-node3 nginx[91561]:         no file '/usr/local/lib/lua/5.1/loadall.so'
May 17 23:15:54 dns-node3 nginx[91561]:         no file './resty.so'
May 17 23:15:54 dns-node3 nginx[91561]:         no file '/usr/local/lib/lua/5.1/resty.so'
May 17 23:15:54 dns-node3 nginx[91561]:         no file '/usr/local/lib/lua/5.1/loadall.so') in /etc/nginx/nginx.conf:117
May 17 23:15:54 dns-node3 systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
...
```

解决方法，

参考 https://github.com/openresty/lua-resty-core/issues/248  切换为 lua-nginx-module-0.10.14.tar.gz
https://blog.csdn.net/budongfengqing/article/details/117925430

参考 https://github.com/openresty/lua-nginx-module/issues/1533 ，

Just clone current project [lua-resty-core](https://github.com/openresty/lua-resty-core)

and setup nginx.conf file regarding the [documentation](https://github.com/openresty/lua-resty-core#synopsis).

```nginx
    # nginx.conf

    http {
        # you do NOT need to configure the following line when you
        # are using the OpenResty bundle 1.4.3.9+.
        lua_package_path "/path/to/lua-resty-core/lib/?.lua;;";

        init_by_lua_block {
            require "resty.core"
            collectgarbage("collect")  -- just to collect any garbage
        }

        ...
    }
```

发现 nginx_1.24.0 + lua-nginx-module-0.10.24.tar.gz 使用这种方法，仍有问题
```bash
May 18 00:36:06 dns-node3 nginx[92546]: nginx: [alert] detected a LuaJIT version which is not OpenResty's; many optimizations will be disabled and performance will be compromised (>
May 18 00:36:06 dns-node3 nginx[92546]: nginx: [alert] failed to load the 'resty.core' module (https://github.com/openresty/lua-resty-core); ensure you are using an OpenResty relea>
May 18 00:36:06 dns-node3 nginx[92546]:         no field package.preload['resty.lrucache']
May 18 00:36:06 dns-node3 nginx[92546]:         no file '/usr/local/lua-resty-core/lib/resty/lrucache.lua'
May 18 00:36:06 dns-node3 nginx[92546]:         no file './resty/lrucache.lua'
May 18 00:36:06 dns-node3 nginx[92546]:         no file '/usr/local/share/luajit-2.1.0-beta3/resty/lrucache.lua'
May 18 00:36:06 dns-node3 nginx[92546]:         no file '/usr/local/share/lua/5.1/resty/lrucache.lua'
May 18 00:36:06 dns-node3 nginx[92546]:         no file '/usr/local/share/lua/5.1/resty/lrucache/init.lua'
May 18 00:36:06 dns-node3 nginx[92546]:         no file './resty/lrucache.so'
May 18 00:36:06 dns-node3 nginx[92546]:         no file '/usr/local/lib/lua/5.1/resty/lrucache.so'
May 18 00:36:06 dns-node3 nginx[92546]:         no file '/usr/local/lib/lua/5.1/loadall.so'
May 18 00:36:06 dns-node3 nginx[92546]:         no file './resty.so'
May 18 00:36:06 dns-node3 nginx[92546]:         no file '/usr/local/lib/lua/5.1/resty.so'
May 18 00:36:06 dns-node3 nginx[92546]:         no file '/usr/local/lib/lua/5.1/loadall.so') in /etc/nginx/nginx.conf:125
```
