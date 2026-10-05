# ============================================================
# MAVEN
# ============================================================

export MAVEN_HOME="/c/Desarrollo/software/Maven/apache-maven-3.9.16-bin/apache-maven-3.9.16"
export PATH="$MAVEN_HOME/bin:$PATH"

mvn() {
    python ~/.bash/functions/maven.py "$@"
}