library(ggplot2)
library(plyr)
library(reshape2)
library(xtable)

setwd("~/scratch/AWS-estimator")

python.times <- read.table("~/scratch/AWS-estimator/python/real-times")[,1]
mean(python.times)
sd(python.times)

r.times <- read.csv("~/scratch/AWS-estimator/R/r-real-times", header = FALSE)
r.times$sec <- r.times$V1 * 60 + r.times$V2
mean(r.times$sec)
sd(r.times$sec)

python <- read.table("~/scratch/AWS-estimator/python/test_python10000")
r <- read.table("~/scratch/AWS-estimator/R/test_R827")

colnames(python) <- c("hours", "num", "price")
colnames(r) <- c("hours", "num", "price")

r2 <- data.frame(matrix(NA, nrow(python), ncol(python)))
r2[1:nrow(r), ] <- r
colnames(r2) <- c("hours", "num", "price")

joined <- cbind(python[, 1:3], r2[, 3])
colnames(joined) <- c("hours", "num", "python", "r")
joined$d <- abs(joined$python - joined$r)
joined$m <- (joined$python + joined$r) / 2
joined$n <- 1:nrow(joined)

j.melt <- melt(joined[1:827, c(1:4, 7)], id=c("hours", "num", "n"))

# Evaluate difference between programs
summary(lm(j.melt$value ~ j.melt$variable))

sum(joined$d / joined$m < .015, na.rm=TRUE) # 801
801 / 827 # 0.9685611

# Average differenceAs 
mean(joined$d, na.rm=TRUE)
sd(joined$d, na.rm=TRUE)

max(joined$d/joined$m, na.rm=TRUE) # 0.04760
mean(joined$d/joined$m, na.rm=TRUE) # 0.007515
sd(joined$d/joined$m, na.rm=TRUE) # 0.006313

# PERCENT ERROR
png("error_percent.png", width=800, height=400)

  ggplot(joined, aes(d/m*100, fill=TRUE)) + 
    geom_density() + 
    xlab("Error (%)") +
    theme(legend.position="none")

dev.off()

joined[which(joined$d/joined$m > .04), ]
xtable(joined[which(joined$d/joined$m > .04), ])

png("bulges.png", width=800, height=400)
  
  ggplot(joined, aes(x=hours, y=num, size=d/m*100)) +
    geom_point() + 
    scale_x_continuous(breaks=1:9, limits=c(1, 9)) +
    xlab("Hours per job") + 
    ylab("Number of jobs") +
    guides(size=guide_legend(title="Percent error"))
  
dev.off()

summary(lm(joined$d/joined$m ~ joined$num + joined$hours))

png("bad-r.png", width=800, height=400)

ggplot(j.melt, aes(num, value, color=variable)) + 
  geom_point() + 
  xlab("Number of jobs") + 
  ylab("Percent error") +
  xlim(c(50, 75))

dev.off()
