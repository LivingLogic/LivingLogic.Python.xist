<?xml version='1.0' encoding='iso-8859-1'?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

	<xsl:template match="/">
	<html>
	<head>
	<h>Media</h>
	<a rel="stylesheet" href="Media.css"/>
	</head>
	<body>
	<h1>Media</h1>
	<xsl:if test="count(media/ld)">
		<h2><xsl:value-of select="count(media/ld)"/> LDs</h2>
		<ol>
			<xsl:for-each select="media/ld">
				<xsl:sort select="name">
					<xsl:apply-templates select="."/>
			</xsc:for-each>
		</ol>
	</xsl:if>
	<xsl:if test="count(media/dvd)">
		<h2><xsl:value-of select="count(media/dvd)"/> DVDs</h2>
		<ol>
			<xsl:for-each select="media/dvd">
				<xsl:sort select="name">
					<xsl:apply-templates select="."/>
			</xsc:for-each>
		</ol>
	</xsl:if>
	</body>
	</html>
	</xsl:template>

	<xsl:template match="dvd">
	<li>
		<span class="name">
			<xsl:value-of select="name"/>
		</span>
		<xsl:if test="duration|rc">
			<xsl:text> (</xsl:text>
			<xsl:apply-templates select="duration"/>
			<xsl:if test="count(duration)">
				<xsl:if test="count(rc)">
					<xsl:text>; </xsl:text>
				</xsl:if>
			</xsl:if>
			<xsl:if test="count(rc)">
				<xsl:text>RC </xsl:text><xsl:apply-templates select="rc"/>
			</xsl:if>
			<xsl:text>)</xsl:text>
		</xsl:if>
		<xsl:apply-templates select="purchase"/>
	</li>
	</xsl:template>

	<xsl:template match="ld">
		<li>
			<span class="name">
				<xsl:value-of select="name"/>
			</span>
			<xsl:if test="count(duration)">
				<xsl:text> (</xsl:text>
				<xsl:value-of select="duration"/>
				<xsl:text> min)</xsl:text>
			</xsl:if>
			<xsl:apply-templates select="purchase"/>
		</li>
	</xsl:template>

	<xsl:template match="duration">
		<xsl:value-of select="."/>
		<xsl:text> min</xsl:text>
	</xsl:template>

	<xsl:template match="rc">
		<xsl:value-of select="."/>
		<xsl:if test="position() != last()">
			<xsl:text>, </xsl:text>
		</xsl:if>
	</xsl:template>

	<xsl:template match="purchase">
		<div class="purchase">
			<xsl:value-of select="place"/>
			<xsl:if test="count(price)">
				<xsl:text>: </xsl:text>
				<xsl:apply-templates select="price"/>
			</xsl:if>
			<xsl:if test="count(date)">
				<xsl:text> </xsl:text>
				<xsl:apply-templates select="date"/>
			</xsl:if>
		</div>
	</xsl:template>

	<xsl:template match="date">
		<xsl:text>(</xsl:text>
		<xsl:value-of select="."/>
		<xsl:text>)</xsl:text>
	</xsl:template>

	<xsl:template match="price">
		<xsl:value-of select="."/>
		<xsl:text> </xsl:text>
		<xsl:value-of select="@currency"/>
	</xsl:template>

</xsl:stylesheet>
