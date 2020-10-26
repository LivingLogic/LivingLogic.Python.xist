# Generated from src/ll/UL4Parser.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .UL4Parser import UL4Parser
else:
    from UL4Parser import UL4Parser

# This class defines a complete generic visitor for a parse tree produced by UL4Parser.

class UL4ParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by UL4Parser#TopLevel.
    def visitTopLevel(self, ctx:UL4Parser.TopLevelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#TagUL4.
    def visitTagUL4(self, ctx:UL4Parser.TagUL4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#TagWhitespace.
    def visitTagWhitespace(self, ctx:UL4Parser.TagWhitespaceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#doctag.
    def visitDoctag(self, ctx:UL4Parser.DoctagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#notetag.
    def visitNotetag(self, ctx:UL4Parser.NotetagContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#name.
    def visitName(self, ctx:UL4Parser.NameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LiteralNone.
    def visitLiteralNone(self, ctx:UL4Parser.LiteralNoneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LiteralFalse.
    def visitLiteralFalse(self, ctx:UL4Parser.LiteralFalseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LiteralTrue.
    def visitLiteralTrue(self, ctx:UL4Parser.LiteralTrueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LiteralInteger.
    def visitLiteralInteger(self, ctx:UL4Parser.LiteralIntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LiteralFloat.
    def visitLiteralFloat(self, ctx:UL4Parser.LiteralFloatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LiteralString.
    def visitLiteralString(self, ctx:UL4Parser.LiteralStringContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LiteralDate.
    def visitLiteralDate(self, ctx:UL4Parser.LiteralDateContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LiteralDatetime.
    def visitLiteralDatetime(self, ctx:UL4Parser.LiteralDatetimeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LiteralColor.
    def visitLiteralColor(self, ctx:UL4Parser.LiteralColorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LiteralName.
    def visitLiteralName(self, ctx:UL4Parser.LiteralNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#SeqItem.
    def visitSeqItem(self, ctx:UL4Parser.SeqItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#UnpackSeqItem.
    def visitUnpackSeqItem(self, ctx:UL4Parser.UnpackSeqItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#ListEmpty.
    def visitListEmpty(self, ctx:UL4Parser.ListEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#List.
    def visitList(self, ctx:UL4Parser.ListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#ListComprehension.
    def visitListComprehension(self, ctx:UL4Parser.ListComprehensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#SetEmpty.
    def visitSetEmpty(self, ctx:UL4Parser.SetEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Set.
    def visitSet(self, ctx:UL4Parser.SetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#SetComprehension.
    def visitSetComprehension(self, ctx:UL4Parser.SetComprehensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#DictItem.
    def visitDictItem(self, ctx:UL4Parser.DictItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#UnpackDictItem.
    def visitUnpackDictItem(self, ctx:UL4Parser.UnpackDictItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#DictEmpty.
    def visitDictEmpty(self, ctx:UL4Parser.DictEmptyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Dict.
    def visitDict(self, ctx:UL4Parser.DictContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#DictComprehension.
    def visitDictComprehension(self, ctx:UL4Parser.DictComprehensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#GeneratorExpresssion.
    def visitGeneratorExpresssion(self, ctx:UL4Parser.GeneratorExpresssionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#AtomLiteral.
    def visitAtomLiteral(self, ctx:UL4Parser.AtomLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#AtomList.
    def visitAtomList(self, ctx:UL4Parser.AtomListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#AtomListComprehension.
    def visitAtomListComprehension(self, ctx:UL4Parser.AtomListComprehensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#AtomSet.
    def visitAtomSet(self, ctx:UL4Parser.AtomSetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#AtomSetComprehension.
    def visitAtomSetComprehension(self, ctx:UL4Parser.AtomSetComprehensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#AtomDict.
    def visitAtomDict(self, ctx:UL4Parser.AtomDictContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#AtomDictComprehension.
    def visitAtomDictComprehension(self, ctx:UL4Parser.AtomDictComprehensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#AtomGeneratorExpression.
    def visitAtomGeneratorExpression(self, ctx:UL4Parser.AtomGeneratorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#AtomBracket.
    def visitAtomBracket(self, ctx:UL4Parser.AtomBracketContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LValueSimple.
    def visitLValueSimple(self, ctx:UL4Parser.LValueSimpleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LValueOne.
    def visitLValueOne(self, ctx:UL4Parser.LValueOneContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LValueMulti.
    def visitLValueMulti(self, ctx:UL4Parser.LValueMultiContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Slice.
    def visitSlice(self, ctx:UL4Parser.SliceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#PosArg.
    def visitPosArg(self, ctx:UL4Parser.PosArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#KeywordArg.
    def visitKeywordArg(self, ctx:UL4Parser.KeywordArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#UnpackListArg.
    def visitUnpackListArg(self, ctx:UL4Parser.UnpackListArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#UnpackDictArg.
    def visitUnpackDictArg(self, ctx:UL4Parser.UnpackDictArgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Add.
    def visitAdd(self, ctx:UL4Parser.AddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#ShiftRight.
    def visitShiftRight(self, ctx:UL4Parser.ShiftRightContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Or.
    def visitOr(self, ctx:UL4Parser.OrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LT.
    def visitLT(self, ctx:UL4Parser.LTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Is.
    def visitIs(self, ctx:UL4Parser.IsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Attr.
    def visitAttr(self, ctx:UL4Parser.AttrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Item.
    def visitItem(self, ctx:UL4Parser.ItemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#BitXOr.
    def visitBitXOr(self, ctx:UL4Parser.BitXOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#IsNot.
    def visitIsNot(self, ctx:UL4Parser.IsNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#GE.
    def visitGE(self, ctx:UL4Parser.GEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Sub.
    def visitSub(self, ctx:UL4Parser.SubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Call.
    def visitCall(self, ctx:UL4Parser.CallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#NotContains.
    def visitNotContains(self, ctx:UL4Parser.NotContainsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Mod.
    def visitMod(self, ctx:UL4Parser.ModContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#BitOr.
    def visitBitOr(self, ctx:UL4Parser.BitOrContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#ShiftLeft.
    def visitShiftLeft(self, ctx:UL4Parser.ShiftLeftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Mul.
    def visitMul(self, ctx:UL4Parser.MulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#ExprAtom.
    def visitExprAtom(self, ctx:UL4Parser.ExprAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#FloorDiv.
    def visitFloorDiv(self, ctx:UL4Parser.FloorDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#EQ.
    def visitEQ(self, ctx:UL4Parser.EQContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#GT.
    def visitGT(self, ctx:UL4Parser.GTContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#TrueDiv.
    def visitTrueDiv(self, ctx:UL4Parser.TrueDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Neg.
    def visitNeg(self, ctx:UL4Parser.NegContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Not.
    def visitNot(self, ctx:UL4Parser.NotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#And.
    def visitAnd(self, ctx:UL4Parser.AndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#BitAnd.
    def visitBitAnd(self, ctx:UL4Parser.BitAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#NE.
    def visitNE(self, ctx:UL4Parser.NEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#Contains.
    def visitContains(self, ctx:UL4Parser.ContainsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#LE.
    def visitLE(self, ctx:UL4Parser.LEContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#ItemSlice.
    def visitItemSlice(self, ctx:UL4Parser.ItemSliceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#BitNot.
    def visitBitNot(self, ctx:UL4Parser.BitNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#If.
    def visitIf(self, ctx:UL4Parser.IfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#exprarg.
    def visitExprarg(self, ctx:UL4Parser.ExprargContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#ExpressionGeneratorExpression.
    def visitExpressionGeneratorExpression(self, ctx:UL4Parser.ExpressionGeneratorExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#ExpressionExpression.
    def visitExpressionExpression(self, ctx:UL4Parser.ExpressionExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#For.
    def visitFor(self, ctx:UL4Parser.ForContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#stmt.
    def visitStmt(self, ctx:UL4Parser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#SignatureNoParams.
    def visitSignatureNoParams(self, ctx:UL4Parser.SignatureNoParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#SignatureUnpackDictParams.
    def visitSignatureUnpackDictParams(self, ctx:UL4Parser.SignatureUnpackDictParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#SignatureUnpackParams.
    def visitSignatureUnpackParams(self, ctx:UL4Parser.SignatureUnpackParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#SignatureDefaultParams.
    def visitSignatureDefaultParams(self, ctx:UL4Parser.SignatureDefaultParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#SignatureAnyParams.
    def visitSignatureAnyParams(self, ctx:UL4Parser.SignatureAnyParamsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#definition.
    def visitDefinition(self, ctx:UL4Parser.DefinitionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#defblock.
    def visitDefblock(self, ctx:UL4Parser.DefblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#forblock.
    def visitForblock(self, ctx:UL4Parser.ForblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#whileblock.
    def visitWhileblock(self, ctx:UL4Parser.WhileblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#ifblock.
    def visitIfblock(self, ctx:UL4Parser.IfblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#renderblockblock.
    def visitRenderblockblock(self, ctx:UL4Parser.RenderblockblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#renderblocksblock.
    def visitRenderblocksblock(self, ctx:UL4Parser.RenderblocksblockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#blockitem.
    def visitBlockitem(self, ctx:UL4Parser.BlockitemContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#TemplateBodyItem.
    def visitTemplateBodyItem(self, ctx:UL4Parser.TemplateBodyItemContext):
        return self.visitChildren(ctx)



del UL4Parser