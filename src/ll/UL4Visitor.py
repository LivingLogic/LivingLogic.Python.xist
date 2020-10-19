# Generated from src/ll/UL4.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .UL4Parser import UL4Parser
else:
    from UL4Parser import UL4Parser

# This class defines a complete generic visitor for a parse tree produced by UL4Parser.

class UL4Visitor(ParseTreeVisitor):

    # Visit a parse tree produced by UL4Parser#float_.
    def visitFloat_(self, ctx:UL4Parser.Float_Context):
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


    # Visit a parse tree produced by UL4Parser#AtomGeneratorComprehension.
    def visitAtomGeneratorComprehension(self, ctx:UL4Parser.AtomGeneratorComprehensionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#AtomIf.
    def visitAtomIf(self, ctx:UL4Parser.AtomIfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#nestedlvalue.
    def visitNestedlvalue(self, ctx:UL4Parser.NestedlvalueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#slice_.
    def visitSlice_(self, ctx:UL4Parser.Slice_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#argument.
    def visitArgument(self, ctx:UL4Parser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expr_subscript.
    def visitExpr_subscript(self, ctx:UL4Parser.Expr_subscriptContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expr_unary.
    def visitExpr_unary(self, ctx:UL4Parser.Expr_unaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expr_mul.
    def visitExpr_mul(self, ctx:UL4Parser.Expr_mulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expr_add.
    def visitExpr_add(self, ctx:UL4Parser.Expr_addContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expr_bitshift.
    def visitExpr_bitshift(self, ctx:UL4Parser.Expr_bitshiftContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expr_bitand.
    def visitExpr_bitand(self, ctx:UL4Parser.Expr_bitandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expr_bitxor.
    def visitExpr_bitxor(self, ctx:UL4Parser.Expr_bitxorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expr_bitor.
    def visitExpr_bitor(self, ctx:UL4Parser.Expr_bitorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expr_cmp.
    def visitExpr_cmp(self, ctx:UL4Parser.Expr_cmpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expr_not.
    def visitExpr_not(self, ctx:UL4Parser.Expr_notContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expr_and.
    def visitExpr_and(self, ctx:UL4Parser.Expr_andContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expr_or.
    def visitExpr_or(self, ctx:UL4Parser.Expr_orContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expr_if.
    def visitExpr_if(self, ctx:UL4Parser.Expr_ifContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#exprarg.
    def visitExprarg(self, ctx:UL4Parser.ExprargContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#expression.
    def visitExpression(self, ctx:UL4Parser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#for_.
    def visitFor_(self, ctx:UL4Parser.For_Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#stmt.
    def visitStmt(self, ctx:UL4Parser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#signature.
    def visitSignature(self, ctx:UL4Parser.SignatureContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by UL4Parser#definition.
    def visitDefinition(self, ctx:UL4Parser.DefinitionContext):
        return self.visitChildren(ctx)



del UL4Parser