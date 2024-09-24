# -*-coding:utf8;-*-
from zcache.Interface.Plugins import Plugins
import pickle
import os
import aiofiles

"""
this plugins is good for large cache
author: guangrei
"""


class AsyncBytesCachePlugins(Plugins):

    useRandomName = True

    async def on_write(db, key, value):  # noqa
        if db.storage.filesystem:
            path = os.path.dirname(db.storage.path)
            darray = db.databases
            if key in darray["data"]:
                filepath = darray["data"][key]["content"]
                if isinstance(filepath, str):
                    if filepath.startswith("pickle://"):
                        filepath = filepath[9:]
                    elif filepath.startswith("bytes://"):
                        filepath = filepath[8:]
                    elif filepath.startswith("text://"):
                        filepath = filepath[7:]
                    else:
                        return value
                else:
                    return value

                if isinstance(value, bytes):
                    if hasattr(db.storage, "write"):
                        await db.storage.write(filepath, value)
                    else:
                        await AsyncBytesCachePlugins.write(filepath, value)
                    return "bytes://" + filepath
                elif isinstance(value, str):
                    if hasattr(db.storage, "write"):
                        await db.storage.write(filepath, value.encode("utf-8"))
                    else:
                        await AsyncBytesCachePlugins.write(
                            filepath, value.encode("utf-8")
                        )
                    return "text://" + filepath
                else:
                    content = await AsyncBytesCachePlugins.pickle_encode(value)
                    if hasattr(db.storage, "write"):
                        await db.storage.write(filepath, content)
                    else:
                        await AsyncBytesCachePlugins.write(filepath, content)
                    return "pickle://" + filepath
            else:
                if AsyncBytesCachePlugins.useRandomName:
                    import uuid

                    filename = ".zcache-" + uuid.uuid4().hex
                else:
                    filename = ".zcache-" + key
                filepath = os.path.join(path, filename)
                if isinstance(value, bytes):
                    if hasattr(db.storage, "write"):
                        await db.storage.write(filepath, value)
                    else:
                        await AsyncBytesCachePlugins.write(filepath, value)
                    return "bytes://" + filepath
                elif isinstance(value, str):
                    if hasattr(db.storage, "write"):
                        await db.storage.write(filepath, value.encode("utf-8"))
                    else:
                        await AsyncBytesCachePlugins.write(
                            filepath, value.encode("utf-8")
                        )
                    return "text://" + filepath
                else:
                    content = await AsyncBytesCachePlugins.pickle_encode(value)
                    if hasattr(db.storage, "write"):
                        await db.storage.write(filepath, content)
                    else:
                        await AsyncBytesCachePlugins.write(filepath, content)
                    return "pickle://" + filepath
        else:
            return value

    async def on_read(db, key, value):
        if db.storage.filesystem:
            if isinstance(value, str):
                filepath = value
                if filepath.startswith("pickle://"):
                    if hasattr(db.storage, "read"):
                        ret = await db.storage.read(filepath[9:])
                    else:
                        ret = await AsyncBytesCachePlugins.read(filepath[9:])
                    return await AsyncBytesCachePlugins.pickle_decode(ret)
                elif filepath.startswith("text://"):
                    if hasattr(db.storage, "read"):
                        ret = await db.storage.read(filepath[7:])
                    else:
                        ret = await AsyncBytesCachePlugins.read(filepath[7:])
                    return ret.decode("utf-8")
                elif filepath.startswith("bytes://"):
                    if hasattr(db.storage, "read"):
                        return await db.storage.read(filepath[8:])
                    else:
                        return await AsyncBytesCachePlugins.read(filepath[8:])
                else:
                    return value
            else:
                return value
        else:
            return value

    async def on_limit():
        pass

    async def on_expired(db, key):
        if db.storage.filesystem:
            filepath = db.databases["data"][key]["content"]
            if isinstance(filepath, str):
                if filepath.startswith("pickle://"):
                    filepath = filepath[9:]
                elif filepath.startswith("bytes://"):
                    filepath = filepath[8:]
                elif filepath.startswith("text://"):
                    filepath = filepath[7:]
                else:
                    return
                if hasattr(db.storage, "delete"):
                    await db.storage.delete(filepath)
                else:
                    os.remove(filepath)

    async def on_delete(db, key):
        if db.storage.filesystem:
            filepath = db.databases["data"][key]["content"]
            if isinstance(filepath, str):
                if filepath.startswith("pickle://"):
                    filepath = filepath[9:]
                elif filepath.startswith("bytes://"):
                    filepath = filepath[8:]
                elif filepath.startswith("text://"):
                    filepath = filepath[7:]
                else:
                    return
                if hasattr(db.storage, "delete"):
                    await db.storage.delete(filepath)
                else:
                    os.remove(filepath)

    async def pickle_encode(data):
        return pickle.dumps(data)

    async def pickle_decode(data):
        return pickle.loads(data)

    async def read(path):
        async with aiofiles.open(path, mode="rb") as f:
            data = await f.read()
        return data

    async def write(path, data):
        async with aiofiles.open(path, mode="wb") as f:
            await f.write(data)
