# Builds the Android app (Khalids-Hunt.apk) with the Android SDK tools only: no Gradle, nothing downloaded.
# Run make_game.py first; it writes assets/index.html (the game with three.js built in).
import glob, os, shutil, subprocess, zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_APK = os.path.join(HERE, "..", "..", "releases", "Khalids-Hunt.apk")
SDK = os.environ.get("ANDROID_HOME") or os.path.join(os.environ["LOCALAPPDATA"], "Android", "Sdk")
BT = os.path.join(SDK, "build-tools", "36.1.0")
if not os.path.isdir(BT):
    BT = sorted(glob.glob(os.path.join(SDK, "build-tools", "*")))[-1]
ANDROID_JAR = os.path.join(sorted(glob.glob(os.path.join(SDK, "platforms", "android-*")))[-1], "android.jar")
JDK = os.environ.get("JAVA_HOME") or r"C:\Program Files\Android\Android Studio\jbr"
JAVA, JAVAC, KEYTOOL = (os.path.join(JDK, "bin", n + ".exe") for n in ("java", "javac", "keytool"))
KEYSTORE = os.path.join(HERE, "rafi-hunt.keystore")   # keep this file: updates must be signed with the same key
PASS = os.environ.get("HUNT_KEYSTORE_PASS") or "rafihunt"   # the key itself (rafi-hunt.keystore) is never published

def run(*cmd):
    print(">", os.path.basename(cmd[0]), *cmd[1:4], "...")
    subprocess.run(cmd, check=True)

build = os.path.join(HERE, "build")
shutil.rmtree(build, ignore_errors=True)
os.makedirs(os.path.join(build, "classes"))
os.makedirs(os.path.join(build, "dex"))
assert os.path.isfile(os.path.join(HERE, "assets", "index.html")), "run make_game.py first"

# 1. resources and manifest
run(os.path.join(BT, "aapt2.exe"), "compile", "--dir", os.path.join(HERE, "res"), "-o", os.path.join(build, "res.zip"))
run(os.path.join(BT, "aapt2.exe"), "link", "-o", os.path.join(build, "base.apk"), "-I", ANDROID_JAR,
    "--manifest", os.path.join(HERE, "AndroidManifest.xml"), "-A", os.path.join(HERE, "assets"), os.path.join(build, "res.zip"))
# 2. Java -> classes -> dex
run(JAVAC, "--release", "11", "-nowarn", "-Xlint:-options", "-classpath", ANDROID_JAR, "-d", os.path.join(build, "classes"),
    *glob.glob(os.path.join(HERE, "src", "**", "*.java"), recursive=True))
classes = glob.glob(os.path.join(build, "classes", "**", "*.class"), recursive=True)
run(JAVA, "-cp", os.path.join(BT, "lib", "d8.jar"), "com.android.tools.r8.D8", "--release", "--min-api", "24",
    "--lib", ANDROID_JAR, "--output", os.path.join(build, "dex"), *classes)
with zipfile.ZipFile(os.path.join(build, "base.apk"), "a", zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(build, "dex", "classes.dex"), "classes.dex")
# 3. align and sign
run(os.path.join(BT, "zipalign.exe"), "-p", "-f", "4", os.path.join(build, "base.apk"), os.path.join(build, "aligned.apk"))
if not os.path.isfile(KEYSTORE):
    run(KEYTOOL, "-genkeypair", "-keystore", KEYSTORE, "-alias", "rafihunt", "-keyalg", "RSA", "-keysize", "2048",
        "-validity", "10000", "-storepass", PASS, "-keypass", PASS, "-dname", "CN=Khalid's Treasure Hunt, O=Village House, C=BD")
run(JAVA, "-jar", os.path.join(BT, "lib", "apksigner.jar"), "sign", "--ks", KEYSTORE, "--ks-pass", "pass:" + PASS,
    "--key-pass", "pass:" + PASS, "--out", OUT_APK, os.path.join(build, "aligned.apk"))
run(JAVA, "-jar", os.path.join(BT, "lib", "apksigner.jar"), "verify", "--verbose", OUT_APK)
print("APK:", os.path.abspath(OUT_APK), os.path.getsize(OUT_APK), "bytes")
