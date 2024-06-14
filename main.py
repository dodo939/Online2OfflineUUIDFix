import hashlib
import os
import re
import uuid


def get_uuid(user_name):
    offline_player_string = "OfflinePlayer:" + user_name
    md5_hash_byte = hashlib.md5(offline_player_string.encode("utf-8")).digest()
    return str(uuid.UUID(bytes=md5_hash_byte, version=3))


def main():
    with open("server.properties", "r") as f:
        config = f.read()
    level_name = re.search(r"level-name\s*=\s*(.+)", config).group(1).strip()

    input(
        f"使用之前请确保请备份以下文件或文件夹: \n    ops.json\n    usercache.json\n    whitelist.json\n    banned-players.json\n    {level_name}/advancements\n    {level_name}/playerdata\n    {level_name}/stats\n按 Enter 继续, 按 Ctrl+C 或者直接关闭窗口退出"
    )

    with open("usercache.json", "r") as f:
        users = f.read()
    offline_uuids = []
    names = re.findall(r'"name":\s*"([^"]+)"', users)
    online_uuids = re.findall(r'"uuid":\s*"([0-9a-fA-F-]+)"', users)

    count = 0
    print("正在从 usercache.json 中生成离线UUID...")
    for name in names:
        offline_uuids.append(get_uuid(name))
        print(f"  {name}: {offline_uuids[count]}")
        count += 1

    print("正在将 ops.json 中玩家 UUID 修改为离线...")
    with open("ops.json", "r+") as f:
        ops = f.read()
        for i in range(count):
            ops = ops.replace(online_uuids[i], offline_uuids[i])
        f.seek(0)
        f.truncate(0)
        f.write(ops)

    print("正在将 banned-players.json 中玩家 UUID 修改为离线...")
    with open("banned-players.json", "r+") as f:
        bans = f.read()
        for i in range(count):
            bans = bans.replace(online_uuids[i], offline_uuids[i])
        f.seek(0)
        f.truncate(0)
        f.write(bans)

    print("正在将 whitelist.json 中玩家 UUID 修改为离线...")
    with open("whitelist.json", "r+") as f:
        wls = f.read()
        for i in range(count):
            wls = wls.replace(online_uuids[i], offline_uuids[i])
        f.seek(0)
        f.truncate(0)
        f.write(wls)

    print("正在将 usercache.json 中玩家 UUID 修改为离线...")
    with open("usercache.json", "r+") as f:
        caches = f.read()
        for i in range(count):
            caches = caches.replace(online_uuids[i], offline_uuids[i])
        f.seek(0)
        f.truncate(0)
        f.write(caches)

    successd = []

    os.chdir(level_name + "/playerdata")
    print(f"正在将 {level_name}/playerdata 中玩家 UUID 修改为离线...")
    for i in range(count):
        try:
            os.remove(offline_uuids[i] + ".dat")
            os.remove(offline_uuids[i] + ".dat_old")
        except:
            pass
        try:
            os.rename(online_uuids[i] + ".dat", offline_uuids[i] + ".dat")
            successd.append(names[i])
            os.rename(online_uuids[i] + ".dat_old", offline_uuids[i] + ".dat_old")
        except:
            pass

    os.chdir("../advancements")
    print(f"正在将 {level_name}/advancements 中玩家 UUID 修改为离线...")
    for i in range(count):
        try:
            os.remove(offline_uuids[i] + ".json")
        except:
            pass
        try:
            os.rename(online_uuids[i] + ".json", offline_uuids[i] + ".json")
        except:
            pass

    os.chdir("../stats")
    print(f"正在将 {level_name}/stats 中玩家 UUID 修改为离线...")
    for i in range(count):
        try:
            os.remove(offline_uuids[i] + ".json")
        except:
            pass
        try:
            os.rename(online_uuids[i] + ".json", offline_uuids[i] + ".json")
        except:
            pass

    print("成功将以下玩家数据转为离线数据: \n\n", successd)
    input("\n按 Enter 退出或者直接关闭窗口")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("\n\n程序出现异常, 请将以下信息发送给开发者\n")
        print(e)
        input()
