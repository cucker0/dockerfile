# nginx_1.26.1


## 问题
### 问题1

journalctl --no-pager -u nginx.service
```bash
May 30 17:16:48 rocky92 nginx[131248]: nginx: [alert] failed to load the 'resty.core' module (https://github.com/openresty/lua-resty-core); ensure you are using an OpenResty release from https://openresty.org/en/download.html (reason: module 'resty.core' not found:
May 30 17:16:48 rocky92 nginx[131248]:         no field package.preload['resty.core']
May 30 17:16:48 rocky92 nginx[131248]:         no file './resty/core.lua'
May 30 17:16:48 rocky92 nginx[131248]:         no file '/usr/local/share/luajit-2.1/resty/core.lua'
May 30 17:16:48 rocky92 nginx[131248]:         no file '/usr/local/share/lua/5.1/resty/core.lua'
May 30 17:16:48 rocky92 nginx[131248]:         no file '/usr/local/share/lua/5.1/resty/core/init.lua'
May 30 17:16:48 rocky92 nginx[131248]:         no file './resty/core.so'
May 30 17:16:48 rocky92 nginx[131248]:         no file '/usr/local/lib/lua/5.1/resty/core.so'
May 30 17:16:48 rocky92 nginx[131248]:         no file '/usr/local/lib/lua/5.1/loadall.so'
May 30 17:16:48 rocky92 nginx[131248]:         no file './resty.so'
May 30 17:16:48 rocky92 nginx[131248]:         no file '/usr/local/lib/lua/5.1/resty.so'
May 30 17:16:48 rocky92 nginx[131248]:         no file '/usr/local/lib/lua/5.1/loadall.so') in /etc/nginx/nginx.conf:117
May 30 17:16:48 rocky92 systemd[1]: nginx.service: Control process exited, code=exited, status=1/FAILURE
...
```

解决方法: 把 lua 模块安装到 LuaJIT 查找的默认 path 下
参考 https://github.com/openresty/lua-resty-core?tab=readme-ov-file#installation

```bash
cd lua-resty-core
sudo make install LUA_LIB_DIR=/usr/local/share/lua/5.1
```


### 问题2
journalctl --no-pager -u nginx.service
```bash
May 30 17:56:04 rocky92 nginx[131474]: nginx: [alert] failed to load the 'resty.core' module (https://github.com/openresty/lua-resty-core); ensure you are using an OpenResty release from https://openresty.org/en/download.html (reason: /usr/local/share/lua/5.1/resty/core/regex.lua:14: module 'resty.lrucache' not found:
May 30 17:56:04 rocky92 nginx[131474]:         no field package.preload['resty.lrucache']
May 30 17:56:04 rocky92 nginx[131474]:         no file '/usr/local/lua-resty-core/lib/resty/lrucache.lua'
May 30 17:56:04 rocky92 nginx[131474]:         no file './resty/lrucache.lua'
May 30 17:56:04 rocky92 nginx[131474]:         no file '/usr/local/share/luajit-2.1/resty/lrucache.lua'
May 30 17:56:04 rocky92 nginx[131474]:         no file '/usr/local/share/lua/5.1/resty/lrucache.lua'
May 30 17:56:04 rocky92 nginx[131474]:         no file '/usr/local/share/lua/5.1/resty/lrucache/init.lua'
May 30 17:56:04 rocky92 nginx[131474]:         no file './resty/lrucache.so'
May 30 17:56:04 rocky92 nginx[131474]:         no file '/usr/local/lib/lua/5.1/resty/lrucache.so'
May 30 17:56:04 rocky92 nginx[131474]:         no file '/usr/local/lib/lua/5.1/loadall.so'
May 30 17:56:04 rocky92 nginx[131474]:         no file './resty.so'
May 30 17:56:04 rocky92 nginx[131474]:         no file '/usr/local/lib/lua/5.1/resty.so'
May 30 17:56:04 rocky92 nginx[131474]:         no file '/usr/local/lib/lua/5.1/loadall.so') in /etc/nginx/nginx.conf:117

```
原因：安装模块 lua-resty-lrucache, module 'resty.core' 依赖此模块

参考 https://github.com/openresty/lua-resty-lrucache/tags
```bash
cd lua-resty-lrucache
sudo make install LUA_LIB_DIR=/usr/local/share/lua/5.1
```